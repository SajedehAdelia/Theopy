import logging
import os
from typing import Any, Dict, List
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.sse import sse_client

logger = logging.getLogger(__name__)


class TeepyMCPClient:
    """
    The MCP Client that connects Theopy (The Brain) to Teepy (The ERP Backend) via HTTP SSE.
    """

    def __init__(self):
        self.teepy_mcp_url = os.getenv("TEEPY_MCP_URL", "http://127.0.0.1:5001/sse")
        self._session = None
        self._exit_stack = None

    async def connect(self):
        """Establish the SSE connection to the Teepy MCP Server."""
        logger.info(
            f"Connecting to Teepy MCP Server via SSE at {self.teepy_mcp_url}..."
        )

        self._exit_stack = AsyncExitStack()

        try:
            sse_transport = await self._exit_stack.enter_async_context(
                sse_client(self.teepy_mcp_url)
            )
            read_stream, write_stream = sse_transport

            self._session = await self._exit_stack.enter_async_context(
                ClientSession(read_stream, write_stream)
            )
            await self._session.initialize()

            logger.info("Successfully connected to Teepy MCP Server via SSE!")
        except Exception as e:
            logger.error(f"Failed to connect to MCP via SSE: {e}")
            raise e

    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """Fetch the list of tools exposed by Teepy (Invoices, Planning, etc.)."""
        if not self._session:
            raise RuntimeError("MCP Client is not connected.")

        tools_response = await self._session.list_tools()

        # Format the tools so Gemini can easily understand them later
        formatted_tools = []
        for tool in tools_response.tools:
            formatted_tools.append(
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema,
                }
            )
        return formatted_tools

    async def call_tool(self, tool_name: str, arguments: dict) -> str:
        """Execute a specific tool on the Teepy server and return the string result."""
        if not self._session:
            raise RuntimeError("MCP Client is not connected.")

        logger.info(f"Calling tool: {tool_name} with args: {arguments}")
        result = await self._session.call_tool(tool_name, arguments)

        # MCP results come back as a list of content blocks. We extract the text.
        if result.content and len(result.content) > 0:
            return result.content[0].text
        return "No data returned."

    async def close(self):
        if self._exit_stack:
            await self._exit_stack.aclose()
            self._session = None
            logger.info("Teepy MCP connection closed.")
