import logging
import os
import sass
import threading
import traceback
import asyncio
from functools import wraps

import requests
from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    redirect,
    session,
    url_for,
)
from dotenv import load_dotenv

from src.auth import TeepyAuthError, authenticate_with_teepy
from src.dispatcher import AgentDispatcher
from src import history_store

load_dotenv()

logger = logging.getLogger(__name__)

app = Flask(__name__)
# Falls back to a fixed dev value so test/CI environments (no .env file) don't
# fail at import time - real deployments set SECRET_KEY via .env. Session
# forgery isn't the primary defense boundary here anyway: every MCP tool call
# is re-authorized against Teepy's own database on the server side.
app.secret_key = os.getenv("SECRET_KEY", "dev-insecure-default-change-in-production")

# One AgentDispatcher per logged-in Teepy user_id, not a single shared
# instance - each dispatcher owns a brain with its own conversation history
# and its own role-filtered tool list, so different users of this Theopy
# instance never see each other's chat or a stale/wrong tool set.
_dispatchers: dict[int, AgentDispatcher] = {}
_dispatchers_lock = threading.Lock()


def _get_dispatcher_for(user_id: int) -> AgentDispatcher:
    with _dispatchers_lock:
        if user_id not in _dispatchers:
            _dispatchers[user_id] = AgentDispatcher()
        return _dispatchers[user_id]


def _discard_dispatcher_for(user_id: int) -> None:
    """Drop a logged-out user's dispatcher, closing its MCP connection and
    freeing its conversation history/tool cache."""
    with _dispatchers_lock:
        stale_dispatcher = _dispatchers.pop(user_id, None)

    if stale_dispatcher is None:
        return

    try:
        asyncio.run(stale_dispatcher.shutdown())
    except Exception as e:
        logger.warning(
            f"Failed to cleanly shut down dispatcher for user_id={user_id}: {e}"
        )


def login_required(view):
    """Gate a route behind a logged-in Theopy session. /ask is an AJAX
    endpoint, so it gets a JSON 401 instead of a redirect."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            if request.path == "/ask":
                return jsonify({"error": "Not authenticated"}), 401
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def compile_sass():
    """
    Logic for the Frontend Asset Pipeline.
    This function automates the conversion of Sass to CSS.
    """
    scss_path = "src/static/style.sass"
    css_path = "src/static/style.css"

    if os.path.exists(scss_path):
        try:
            with open(css_path, "w") as f:
                f.write(sass.compile(filename=scss_path))
            print(" SUCCESS: Sass compiled to CSS.")
        except Exception as e:
            print(f" ERROR: Sass failed to compile: {e}")
    else:
        print(" WARNING: style.sass not found. Skipping compilation.")


compile_sass()

# --- ROUTES ---


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "user_id" in session:
            return redirect(url_for("index"))
        return render_template("login.html.jinja2")

    login_value = request.form.get("login", "").strip()
    password = request.form.get("password", "")

    if not login_value or not password:
        return (
            render_template(
                "login.html.jinja2",
                error="Identifiant et mot de passe requis.",
                login=login_value,
            ),
            400,
        )

    try:
        profile = authenticate_with_teepy(login_value, password)
    except TeepyAuthError as e:
        return (
            render_template("login.html.jinja2", error=str(e), login=login_value),
            401,
        )
    except requests.RequestException:
        return (
            render_template(
                "login.html.jinja2",
                error="Impossible de contacter Teepy. Réessayez plus tard.",
                login=login_value,
            ),
            503,
        )

    session["user_id"] = profile["user_id"]
    session["login"] = profile["login"]
    session["name"] = profile["name"]
    session["role"] = profile["role"]

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    user_id = session.get("user_id")
    session.clear()
    if user_id is not None:
        _discard_dispatcher_for(user_id)
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    return render_template(
        "theopy-chat.html.jinja2",
        title="Theopy AI",
        user_name=session.get("name"),
        user_login=session.get("login"),
        user_role=session.get("role"),
    )


@app.route("/ask", methods=["POST"])
@login_required
def ask_theopy():
    """The bridge between the Frontend UI and the AI Dispatcher."""
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Reuse this user's own dispatcher (not a fresh one) so the brain's
        # conversation history survives across messages in the same session,
        # without leaking into any other logged-in user's dispatcher.
        dispatcher = _get_dispatcher_for(session["user_id"])
        ai_response = asyncio.run(
            dispatcher.handle_user_input(
                user_input, session["user_id"], session["role"]
            )
        )

        return jsonify({"response": ai_response})

    except Exception as e:  # noqa: F841
        print("\n--- THEOPY CRASH REPORT ---")
        traceback.print_exc()
        print("---------------------------\n")
        return jsonify({"error": "I'm having trouble connecting right now."}), 500


@app.route("/health", methods=["GET"])
def health():
    """DevOps Supervision endpoint for Docker health checks."""
    return jsonify({"status": "healthy", "service": "Theopy-Agent"}), 200


@app.route("/history", methods=["GET"])
@login_required
def get_history():
    """Returns the last 24h of MCP tool calls, grouped by business domain."""
    return jsonify(history_store.get_grouped()), 200


if __name__ == "__main__":
    # Running on 0.0.0.0 is mandatory for Docker access
    app.run(host="0.0.0.0", port=8000, debug=True)
