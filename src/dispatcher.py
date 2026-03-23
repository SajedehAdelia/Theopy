import requests
from flask import current_app
from .intent_definitions import INTENT_MAP

class Dispatcher:
    def __init__(self, base_url="http://app:5000"):
        self.base_url = base_url

    def execute_tool(self, tool_call):
        """
        Processes a tool call from Gemini.
        tool_call format: {'name': 'get_customer_sessions', 'arguments': {'customer_name': '...'}}
        """
        tool_name = tool_call.get("name")
        args = tool_call.get("arguments", {})

        # Mapping tool names to our Internal Intent Map
        mapping = {
            "get_customer_sessions": "CUSTOMER_SESSION",
            "get_invoice_summary": "INVOICE_SUMMARY",
            "open_session_page": "CUSTOMER_SESSION" 
        }

        intent_key = mapping.get(tool_name)
        if not intent_key:
            return {"error": f"Tool {tool_name} not recognized by Dispatcher."}

        config = INTENT_MAP[intent_key]
        url = f"{self.base_url}{config['route']}"
        
            # We pass customer_name as a query parameter for GET requests
            params = {}
            if "customer_name" in args:
                params["q"] = args["customer_name"]

            response = requests.request(
                method=config["method"],
                url=url,
                params=params,
                timeout=5
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            return {"error": f"Connection to Teepy failed: {str(e)}"}

    def handle_navigation(self, tool_name, data):
        """
        Special logic for 'open_session_page' to tell the Frontend where to go.
        """
        if tool_name == "open_session_page":
            return {"action": "NAVIGATE", "target": "session_view", "data": data}
        return None