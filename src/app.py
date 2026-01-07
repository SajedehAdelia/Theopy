import os
import sass
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from openai import OpenAI

# Load configuration from .env (Secret management is an RNCP requirement)
load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

def get_ai_response(user_input):
    """
    Core AI logic that maps user requests to Theopy's context.
    This will eventually handle OpenAI Function Calling to interact with Teepy.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "I am Theopy, a professional AI assistant for Teepy (Kozea). "
                        "I help kozea manage invoices and tiers-payant flows. "
                        "Keep responses helpful, technical, and concise."
                    )
                },
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Theopy Gateway Error: {str(e)}"

# --- ROUTES ---

@app.route('/')
def index():
    """Renders the main Jinja2 interface"""
    # Passing variables to Jinja2 to demonstrate dynamic rendering
    return render_template('index.html.jinja2', 
                           title="Theopy AI", 
                           user_status="Pharmacy Admin")

@app.route('/health', methods=['GET'])
def health():
    """Monitoring endpoint for DevOps (Block 3)"""
    return jsonify({"status": "healthy", "service": "Theopy-Gateway"}), 200

@app.route('/v1/chat', methods=['POST'])
def chat():
    """Main Ingress API for text interaction"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400

        user_input = data['message']
        ai_reply = get_ai_response(user_input)
        
        return jsonify({
            "reply": ai_reply,
            "status": "success"
        }), 200

    except Exception as e:
        app.logger.error(f"Chat Error: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500

if __name__ == '__main__':
    # Running on 0.0.0.0 is mandatory for Docker access
    app.run(host='0.0.0.0', port=8000, debug=True)