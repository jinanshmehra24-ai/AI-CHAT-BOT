"""
Simple AI Chatbot — Website Version
--------------------------------------
Same chatbot as chatbot.py, now with a browser-based chat UI:
sidebar with recent chats, new chat button, copy button on replies,
and instant answers when you repeat a question you already asked.

HOW TO RUN:
  1. Install dependencies:
       pip install flask google-genai gunicorn --break-system-packages
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
import uuid

from flask import Flask, render_template, request, jsonify, session

try:
    from google import genai
except ImportError:
    print("Missing dependency. Run this first:")
    print("  pip install flask google-genai gunicorn --break-system-packages")
    sys.exit(1)

# ---- Config ----
API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = "gemini-3.5-flash-lite"  # fastest model — swap to "gemini-3.6-flash" for smarter but slower replies
SYSTEM_PROMPT = (
    "You are a friendly, helpful assistant chatting with a beginner who is "
    "learning to build AI projects. Keep answers clear and not too long, "
    "unless the user asks for detail."
)
TITLE_MAX_LEN = 40

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

# ---- In-memory data store ----
# users[sid] = {
#     "conversations": {
#         conv_id: {
#             "title": str,
#             "prev_id": str | None,       # Gemini's previous_interaction_id, for memory
#             "messages": [{"role": "user"|"bot", "text": str}, ...],
#             "cache": {question_lowercased: answer},  # instant repeat answers
#         },
#         ...
#     },
#     "active": conv_id | None,
# }
# NOTE: this all lives in memory, so it resets whenever the server restarts
# (e.g. a free Render instance waking up from sleep). That's fine for a
# learning project — for anything real you'd use a database instead.
users = {}


def get_user():
    """Get (or create) this visitor's record, keyed by a cookie."""
    sid = session.get("sid")
    if sid is None or sid not in users:
        sid = uuid.uuid4().hex
        session["sid"] = sid
        users[sid] = {"conversations": {}, "active": None}
    return users[sid]


def new_conversation(user):
    conv_id = uuid.uuid4().hex
    user["conversations"][conv_id] = {
        "title": "New chat",
        "prev_id": None,
        "messages": [],
        "cache": {},
    }
    user["active"] = conv_id
    return conv_id


def make_title(text: str) -> str:
    text = text.strip().replace("\n", " ")
    if len(text) > TITLE_MAX_LEN:
        return text[:TITLE_MAX_LEN].rstrip() + "…"
    return text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/conversations", methods=["GET"])
def list_conversations():
    user = get_user()
    if not user["conversations"]:
        new_conversation(user)
    items = [{"id": cid, "title": c["title"]} for cid, c in user["conversations"].items()]
    items.reverse()  # newest first
    return jsonify({"conversations": items, "active": user["active"]})


@app.route("/api/conversations/new", methods=["POST"])
def create_conversation():
    user = get_user()
    conv_id = new_conversation(user)
    return jsonify({"id": conv_id})


@app.route("/api/conversations/<conv_id>", methods=["GET"])
def get_conversation(conv_id):
    user = get_user()
    conv = user["conversations"].get(conv_id)
    if not conv:
        return jsonify({"error": "Not found"}), 404
    user["active"] = conv_id
    return jsonify({"id": conv_id, "title": conv["title"], "messages": conv["messages"]})


@app.route("/api/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json(force=True)
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    user = get_user()
    conv_id = user["active"]
    if not conv_id or conv_id not in user["conversations"]:
        conv_id = new_conversation(user)
    conv = user["conversations"][conv_id]

    is_first_message = len(conv["messages"]) == 0
    cache_key = user_message.lower()

    # Speed trick: if this exact question was already asked in this chat,
    # skip the API call entirely and reuse the saved answer.
    if cache_key in conv["cache"]:
        reply = conv["cache"][cache_key]
        cached = True
    else:
        try:
            interaction = client.interactions.create(
                model=MODEL,
                input=user_message,
                system_instruction=SYSTEM_PROMPT,
                previous_interaction_id=conv["prev_id"],
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        reply = interaction.output_text
        conv["prev_id"] = interaction.id
        conv["cache"][cache_key] = reply
        cached = False

    conv["messages"].append({"role": "user", "text": user_message})
    conv["messages"].append({"role": "bot", "text": reply})
    if is_first_message:
        conv["title"] = make_title(user_message)

    return jsonify({
        "reply": reply,
        "conversation_id": conv_id,
        "title": conv["title"],
        "cached": cached,
    })


@app.route("/api/conversations/<conv_id>/activate", methods=["POST"])
def activate_conversation(conv_id):
    user = get_user()
    if conv_id not in user["conversations"]:
        return jsonify({"error": "Not found"}), 404
    user["active"] = conv_id
    return jsonify({"ok": True})


@app.route("/api/conversations/<conv_id>", methods=["DELETE"])
def delete_conversation(conv_id):
    user = get_user()
    if conv_id in user["conversations"]:
        del user["conversations"][conv_id]
        if user["active"] == conv_id:
            user["active"] = None
    return jsonify({"ok": True})


if __name__ == "__main__":
    # Hosting services (like Render) tell the app which port to use via
    # the PORT environment variable. Locally, that's not set, so we
    # default to 5000.
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    print(f"\nChatbot running at http://localhost:{port}")
    print("Same WiFi pe doosre log tumhari IP se access kar sakte hain (README dekho).\n")
    app.run(host="0.0.0.0", debug=debug_mode, port=port)
