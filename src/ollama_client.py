import os
import json
import logging
from openai import OpenAI

from src.response_guard import sanitize_final_answer
from src.system_prompt import THEOPY_SYSTEM_INSTRUCTION

logger = logging.getLogger(__name__)


class OllamaBrain:
    def __init__(self, mcp_client):
        self.mcp_client = mcp_client

        # 'host.docker.internal' is Docker's magic bridge to Mac's localhost
        self.client = OpenAI(
            base_url="http://host.docker.internal:11434/v1",
            api_key="dummy-key-not-needed",
        )
        self.model_id = os.getenv("OLLAMA_MODEL", "llama3.1")
        # Persisted across calls so the conversation history (previous turns)
        # is preserved across messages, instead of resetting every time.
        self.messages = [{"role": "system", "content": THEOPY_SYSTEM_INSTRUCTION}]
        self.openai_tools = None
        # Keep at most this many non-system messages, to bound token growth
        # over a long-running conversation.
        self.max_history_messages = 40

    def _convert_mcp_to_openai_tools(self, mcp_tools) -> list:
        """Converts MCP JSON Schemas into OpenAI/Ollama Function Declarations."""
        openai_tools = []
        for tool in mcp_tools:
            openai_tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool["description"],
                        "parameters": tool.get(
                            "inputSchema", {"type": "object", "properties": {}}
                        ),
                    },
                }
            )
        return openai_tools

    def _trim_history(self):
        """Keep the system message plus only the most recent turns, so the
        conversation doesn't grow unbounded over a long-running session."""
        system_message = self.messages[0]
        rest = self.messages[1:]
        max_messages = self.max_history_messages
        if len(rest) > max_messages:
            rest = rest[-max_messages:]
        self.messages = [system_message] + rest

    async def process_user_request(self, user_text: str) -> str:
        """The main Agent Loop using the Local LLM."""

        if self.openai_tools is None:
            mcp_tools = await self.mcp_client.get_available_tools()
            self.openai_tools = self._convert_mcp_to_openai_tools(mcp_tools)

        self.messages.append({"role": "user", "content": user_text})
        self._trim_history()
        messages = self.messages

        logger.info(f"User asked Local AI: {user_text}")

        # Initial request to the local model
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            tools=self.openai_tools,
            temperature=0,
        )

        response_message = response.choices[0].message
        messages.append(response_message)

        # Handle Tool Calling Loop
        while response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                logger.info(
                    f"🧠 Local AI requested tool: {tool_name} with args: {tool_args}"
                )

                try:
                    mcp_result = await self.mcp_client.call_tool(tool_name, tool_args)
                except Exception as e:
                    mcp_result = f"Error executing tool: {str(e)}"
                    logger.error(mcp_result)

                # Append the tool result to the conversation history
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": str(mcp_result),
                    }
                )

            # Send the results back to the local model so it can formulate a final answer
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                tools=self.openai_tools,
                temperature=0,
            )
            response_message = response.choices[0].message
            messages.append(response_message)

        return sanitize_final_answer(response_message.content)
