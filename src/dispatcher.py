import logging
import os
from dotenv import load_dotenv

from src.mcp_client import TeepyMCPClient
from src.gemini_client import TheopyBrain

load_dotenv()

logger = logging.getLogger(__name__)

class AgentDispatcher:
    def __init__(self):
        self.teepy_path = os.getenv("TEEPY_PATH")
        if not self.teepy_path:
            raise ValueError("TEEPY_PATH is not set in the .env file!")
            
        self.mcp_client = TeepyMCPClient(self.teepy_path)
        self.brain = None

    async def initialize(self):
        """Connects to the ERP and wakes up the AI Brain."""
        await self.mcp_client.connect()
        self.brain = TheopyBrain(self.mcp_client)
        logger.info("Theopy Dispatcher initialized and ready.")

    async def handle_user_input(self, text: str) -> str:
        """Receives text from the Siri UI and returns the AI's spoken response."""
        if not self.brain:
            await self.initialize()
            
        logger.info("Processing user request...")
        final_answer = await self.brain.process_user_request(text)
        return final_answer

    async def shutdown(self):
        await self.mcp_client.close()

