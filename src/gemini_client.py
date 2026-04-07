import os
import google.generativeai as genai
from intent_definitions import TOOLS

class GeminiCoordinator:
    def __init__(self):
        # Load API Key from .env (the file we just fixed on Linux!)
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        
        # System Instruction: This is the "Employee Handbook"
        self.instruction = (
            "You are Theopy, the AI Coordinator for Teepy. "
            "Your goal is to help manage pharmacy sessions and invoices. "
            "Use the provided tools to fetch data or navigate the app. "
            "If a customer name is mentioned, extract it for the tool call."
        )
        
        # Initialize the model with our virtual tools
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            tools=TOOLS,
            system_instruction=self.instruction
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=False)

    def ask(self, user_text):
        """
        Sends text to Gemini and returns the decision (Text or Tool Call).
        """
        response = self.chat.send_message(user_text)
        
        # Check if Gemini wants to use a tool
        if response.candidates[0].content.parts[0].function_call:
            fn = response.candidates[0].content.parts[0].function_call
            return {
                "type": "tool_call",
                "name": fn.name,
                "arguments": dict(fn.args)
            }
        
        # Otherwise, it's just a regular text reply
        return {
            "type": "text",
            "content": response.text
        }