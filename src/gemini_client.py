import os
import logging
from google import genai
from google.genai import types

from src.response_guard import sanitize_final_answer
from src.system_prompt import THEOPY_SYSTEM_INSTRUCTION

logger = logging.getLogger(__name__)


class GeminiBrain:
    def __init__(self, mcp_client):
        self.mcp_client = mcp_client

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing from the environment!")

        self.client = genai.Client(api_key=api_key)
        self.model_id = os.getenv("GEMINI_MODEL_ID", "gemini-2.5-flash")
        self.chat = None  # Created once on first message, then reused so the
        # conversation history (previous turns) is preserved across messages.

    def _convert_mcp_to_gemini_tools(self, mcp_tools) -> list:
        """Converts MCP JSON Schemas into Gemini Function Declarations."""
        gemini_functions = []
        for tool in mcp_tools:

            func_decl = types.FunctionDeclaration(
                name=tool["name"],
                description=tool["description"],
                parameters=tool.get("inputSchema", {}),
            )
            gemini_functions.append(func_decl)

        return [types.Tool(function_declarations=gemini_functions)]

    async def process_user_request(self, user_text: str) -> str:
        """The main Agent Loop: Reason, Act, Observe, Respond."""

        # Tags any tool calls made during this turn with the question that
        # triggered them, so the 24h history can show "what you asked".
        self.mcp_client.current_question = user_text

        if self.chat is None:
            mcp_tools = await self.mcp_client.get_available_tools()
            gemini_tools = self._convert_mcp_to_gemini_tools(mcp_tools)

            config = types.GenerateContentConfig(
                system_instruction=THEOPY_SYSTEM_INSTRUCTION,
                tools=gemini_tools,
                temperature=0,
            )
            self.chat = self.client.chats.create(model=self.model_id, config=config)

        chat = self.chat
        logger.info(f"User asked: {user_text}")

        response = chat.send_message(user_text)

        while response.function_calls:
            for tool_call in response.function_calls:
                tool_name = tool_call.name
                tool_args = tool_call.args if isinstance(tool_call.args, dict) else {}

                logger.info(
                    f"🧠 Gemini requested tool: {tool_name} with args: {tool_args}"
                )

                try:
                    mcp_result = await self.mcp_client.call_tool(tool_name, tool_args)
                except Exception as e:
                    mcp_result = f"Error executing tool: {str(e)}"
                    logger.error(mcp_result)

                logger.info(
                    f" Tool returned data (length {len(mcp_result)}). Sending back to Gemini..."
                )

                response = chat.send_message(
                    types.Part.from_function_response(
                        name=tool_name, response={"result": mcp_result}
                    )
                )

        return sanitize_final_answer(response.text)
