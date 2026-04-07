from dispatcher import Dispatcher
from gemini_client import GeminiCoordinator
import os
import sass
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai
import sys


# 1. Point Python to the 'window' created in Docker
# This allows 'import teepy' to work even if the files aren't in 'src'
sys.path.append('/app/teepy_source')

try:
    from teepy.repositories.invoice import InvoiceRepository
    print("Successfully linked to Teepy Repositories")
except ImportError as e:
    print(f"Could not find Teepy source: {e}")

# Load configuration from .env (Secret management is an RNCP requirement)
load_dotenv()

app = Flask(__name__)

# Initialize AI and Dispatcher
ai_coordinator = GeminiCoordinator()
dispatcher = Dispatcher(base_url="http://app:5000")

# Configure Gemini
if os.getenv("GEMINI_API_KEY"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def compile_sass():
    """
    Logic for the Frontend Asset Pipeline.
    This function automates the conversion of Sass to CSS.
    """
    scss_path = 'src/static/style.sass'
    css_path = 'src/static/style.css'
    
    if os.path.exists(scss_path):
        try:
            # sass.compile reads the scss file and returns a string of pure CSS.
            with open(css_path, 'w') as f:
                f.write(sass.compile(filename=scss_path))
            print(" SUCCESS: Sass compiled to CSS.")
        except Exception as e:
            print(f" ERROR: Sass failed to compile: {e}")
    else:
        print(" WARNING: style.sass not found. Skipping compilation.")

compile_sass()

# --- ROUTES ---

@app.route('/')
def index():
    """Renders the main Jinja2 interface"""
    # Passing variables to Jinja2 to demonstrate dynamic rendering
    return render_template('index.html.jinja2', 
                           title="Theopy AI")

@app.route('/ask', methods=['POST'])
def ask_theopy():
    """
    Main Orchestrator Route. 
    Validates C2.2.3 by handling complex AI-driven logic.
    """
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # The AI Coordinator decides if we need data or just chat
    ai_response = ai_coordinator.ask(user_input)

    if ai_response["type"] == "tool_call":
        # Execute the Teepy API call via the Dispatcher
        data = dispatcher.execute_tool(ai_response)
        
        # Check for UI navigation (Expert Title: Interaction Logic)
        nav = dispatcher.handle_navigation(ai_response["name"], data)
        if nav:
            return jsonify(nav)

        return jsonify({
            "action": "DISPLAY_DATA",
            "intent": ai_response["name"],
            "data": data
        })

    # Standard AI reply
    return jsonify({
        "action": "SPEAK",
        "content": ai_response["content"]
    })

@app.route('/health', methods=['GET'])
def health():
    """Supervision endpoint (Requirement C4.1.2)"""
    return jsonify({"status": "healthy", "service": "Theopy-Gateway"}), 200

if __name__ == '__main__':
    # Running on 0.0.0.0 is mandatory for Docker access
    app.run(host='0.0.0.0', port=8000, debug=True)