import os
import sass
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

from src.dispatcher import AgentDispatcher

load_dotenv()

app = Flask(__name__)

dispatcher = AgentDispatcher()

def compile_sass():
    """
    Logic for the Frontend Asset Pipeline.
    This function automates the conversion of Sass to CSS.
    """
    scss_path = 'src/static/style.sass'
    css_path = 'src/static/style.css'
    
    if os.path.exists(scss_path):
        try:
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
    return render_template('index.html.jinja2', title="Theopy AI")

@app.route('/ask', methods=['POST'])
async def ask_theopy():
    """The bridge between the Frontend UI and the AI Dispatcher."""
    user_input = request.json.get("message")
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        ai_response = await dispatcher.handle_user_input(user_input)
        
        return jsonify({"response": ai_response})
        
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": "I'm having trouble connecting right now."}), 500

@app.route('/health', methods=['GET'])
def health():
    """DevOps Supervision endpoint for Docker health checks."""
    return jsonify({"status": "healthy", "service": "Theopy-Agent"}), 200

if __name__ == '__main__':
    # Running on 0.0.0.0 is mandatory for Docker access
    app.run(host='0.0.0.0', port=8000, debug=True)