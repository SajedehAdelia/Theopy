from dispatcher import Dispatcher
from gemini_client import GeminiCoordinator
import os
import sass
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai
import sys


sys.path.append('/app/teepy_source')

try:
    from teepy.repositories.invoice import InvoiceRepository
    print("Successfully linked to Teepy Repositories")
except ImportError as e:
    print(f"Could not find Teepy source: {e}")

load_dotenv()

app = Flask(__name__)

ai_coordinator = GeminiCoordinator()
dispatcher = Dispatcher(base_url="http://app:5000")


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
    return render_template('index.html.jinja2', 
                           title="Theopy AI")

@app.route('/ask', methods=['POST'])
def ask_theopy():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    ai_response = ai_coordinator.ask(user_input)

    if ai_response["type"] == "tool_call":
        data = dispatcher.execute_tool(ai_response)
        nav = dispatcher.handle_navigation(ai_response["name"], data)
        if nav:
            return jsonify(nav)

        return jsonify({
            "action": "DISPLAY_DATA",
            "intent": ai_response["name"],
            "data": data
        })

    return jsonify({
        "action": "SPEAK",
        "content": ai_response["content"]
    })

@app.route('/health', methods=['GET'])
def health():
    """Supervision endpoint"""
    return jsonify({"status": "healthy", "service": "Theopy-Gateway"}), 200

if __name__ == '__main__':
    # Running on 0.0.0.0 is mandatory for Docker access
    app.run(host='0.0.0.0', port=8000, debug=True)