import os
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


class TheopyBrain:
    def __init__(self, mcp_client):
        self.mcp_client = mcp_client

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing from the environment!")

        self.client = genai.Client(api_key=api_key)
        self.model_id = os.getenv("GEMINI_MODEL_ID", "gemini-2.5-flash")

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

        mcp_tools = await self.mcp_client.get_available_tools()
        gemini_tools = self._convert_mcp_to_gemini_tools(mcp_tools)

        system_instruction = (
            "You are Theopy, the intelligent AI voice assistant for the Teepy ERP system. "
            "Your job is to help managers and operators manage their planning, invoices, and sessions. "
            "Always use your tools to fetch real data before answering. "
            "Be concise, professional, and friendly. Do not output raw JSON or markdown tables to the user, "
            "just speak naturally as if you were an advanced Siri or Jarvis."
        )

        config = types.GenerateContentConfig(
            system_instruction=system_instruction, tools=gemini_tools
        )

        chat = self.client.chats.create(model=self.model_id, config=config)
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

        return response.text
