import os
import logging
from dotenv import load_dotenv

from src.mcp_client import TeepyMCPClient

load_dotenv()

logger = logging.getLogger(__name__)


class AgentDispatcher:
    def __init__(self):
        self.mcp_client = TeepyMCPClient()
        self.brain = None

    async def initialize(self):
        """Connect to the backend and initialize the Brain."""
        await self.mcp_client.connect()

        if os.getenv("USE_LOCAL_LLM") == "1":
            from .ollama_client import OllamaBrain

            self.brain = OllamaBrain(self.mcp_client)
            print("🧠 Booting Theopy with LOCAL OLLAMA Model")
        else:
            from .gemini_client import GeminiBrain

            self.brain = GeminiBrain(self.mcp_client)
            print("🧠 Booting Theopy with CLOUD GEMINI Model")

    async def handle_user_input(self, text: str) -> str:
        """Receives text from the Siri UI and returns the AI's spoken response."""
        if not self.brain:
            await self.initialize()
        try:
            logger.info("Processing user request...")
            final_answer = await self.brain.process_user_request(text)
            return final_answer
        finally:
            if hasattr(self, "mcp_client") and self.mcp_client:
                await self.mcp_client.close()

    async def shutdown(self):
        await self.mcp_client.close()
