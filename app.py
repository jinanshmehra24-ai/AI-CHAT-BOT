"""
Simple AI Chatbot — Website Version
--------------------------------------
Same chatbot as chatbot.py, now with a browser-based chat UI.

HOW TO RUN:
  1. Install dependencies:
       pip install flask google-genai --break-system-packages
  2. Get a free API key (if you don't have one): https://aistudio.google.com/apikey
  3. Set it as an environment variable, OR paste it in when asked.
       (Mac/Linux)  export GEMINI_API_KEY="your-key-here"
       (Windows)    setx GEMINI_API_KEY "your-key-here"
  4. Run it:
       python app.py
  5. Open your browser to:
       http://localhost:5000
"""

import os
import sys

from flask import Flask, render_template, request, jsonify, session

try:
    from google import genai
except ImportError:
    print("Missing dependency. Run this first:")
    print("  pip install flask google-genai --break-system-packages")
    sys.exit(1)

# ---- Config ----
API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = "gemini-3.5-flash-lite"  # fastest model — swap to "gemini-3.6-flash" for smarter but slower replies
SYSTEM_PROMPT = (
    "You are a friendly, helpful assistant chatting with a beginner who is "
    "learning to build AI projects. Keep answers clear and not too long, "
    "unless the user asks for detail."
)

if not API_KEY:
    # On a hosting service there's no one to type a key in, so just ask
    # for it locally. When deploying live, set GEMINI_API_KEY in the
    # host's dashboard instead (see README).
    if sys.stdin.isatty():
        print("No GEMINI_API_KEY environment variable found.")
        API_KEY = input("Paste your Gemini API key here: ").strip()
    if not API_KEY:
        print("No key provided. Set the GEMINI_API_KEY environment variable. Exiting.")
        sys.exit(1)

client = genai.Client(api_key=API_KEY)

app = Flask(__name__)
app.secret_key = os.urandom(24)  # needed for session cookies (per-visitor memory)

# In-memory store: { session_id: previous_interaction_id }
# NOTE: this resets whenever the server restarts, and only works for one
# server process. That's fine for learning/local use.
sessions = {}


def get_session_id():
    """Get (or create) this visitor's session id, so each browser tab
    has its own independent conversation memory."""
    sid = session.get("sid")
    if sid is None:
        sid = os.urandom(8).hex()
        session["sid"] = sid
        sessions[sid] = None
    return sid


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json(force=True)
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    sid = get_session_id()
    previous_interaction_id = sessions.get(sid)

    try:
        interaction = client.interactions.create(
            model=MODEL,
            input=user_message,
            system_instruction=SYSTEM_PROMPT,
            previous_interaction_id=previous_interaction_id,
        )
        sessions[sid] = interaction.id
        return jsonify({"reply": interaction.output_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/clear", methods=["POST"])
def clear_endpoint():
    sid = session.get("sid")
    if sid:
        sessions[sid] = None
    return jsonify({"ok": True})


if __name__ == "__main__":
    # Hosting services (like Render) tell the app which port to use via
    # the PORT environment variable. Locally, that's not set, so we
    # default to 5000.
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    print(f"\nChatbot running at http://localhost:{port}")
    print("Same WiFi pe doosre log tumhari IP se access kar sakte hain (README dekho).\n")
    # host="0.0.0.0" means: listen on all network interfaces, not just this PC.
    # This is what lets other devices (or the internet, once deployed) reach it.
    app.run(host="0.0.0.0", debug=debug_mode, port=port)
