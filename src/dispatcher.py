import os
import logging
from dotenv import load_dotenv

from src import history_store
from src.mcp_client import TeepyMCPClient

load_dotenv()

logger = logging.getLogger(__name__)


class AgentDispatcher:
    def __init__(self):
        self.mcp_client = TeepyMCPClient()
        self.brain = None

    async def initialize(self):
        """Reconnect the MCP client (done every turn - the SSE connection is
        closed after each message) and create the Brain once. The brain is only
        created the first time so its conversation history persists across turns."""
        await self.mcp_client.connect()

        if self.brain is not None:
            return

        if os.getenv("USE_LOCAL_LLM") == "1":
            from .ollama_client import OllamaBrain

            self.brain = OllamaBrain(self.mcp_client)
            print("🧠 Booting Theopy with LOCAL OLLAMA Model")
        else:
            from .gemini_client import GeminiBrain

            self.brain = GeminiBrain(self.mcp_client)
            print("🧠 Booting Theopy with CLOUD GEMINI Model")

    async def handle_user_input(self, text: str, user_id: int, role: str) -> str:
        """Receives text from the chat UI and returns the AI's spoken response.

        user_id is the Teepy user_id from the logged-in Flask session - it is
        carried on every MCP tool call so Teepy can enforce the real caller's
        role, never trusted from anything the LLM itself reports. role is used
        only to filter the tool list shown to the LLM (a UX nicety - see
        src/role_access.py); Teepy's own server-side check is authoritative."""
        await self.initialize()
        self.mcp_client.current_user_id = user_id
        self.mcp_client.current_user_role = role
        try:
            logger.info("Processing user request...")
            final_answer = await self.brain.process_user_request(text)
            try:
                history_store.attach_final_answer(user_id, text, final_answer)
            except Exception as e:
                # Same convenience-side-effect guarantee as recording itself
                # (see mcp_client.call_tool) - never break the real answer.
                logger.warning(f"Failed to attach final answer to history: {e}")
            return final_answer
        finally:
            if hasattr(self, "mcp_client") and self.mcp_client:
                await self.mcp_client.close()

    async def shutdown(self):
        await self.mcp_client.close()
