"""
app.py
Flask backend for the Knowledge Assistant chatbot.
"""

import os
from flask import Flask, render_template, request, jsonify, session
from chatbot_logic import get_response

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def index():
    """Render the main chat interface."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Receive a user message (JSON) and return the chatbot response (JSON).
    Expects:  { "message": "<user text>" }
    Returns:  { "response": "<bot reply>" }
    """
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please type a message first! 😊"})

    current_state = session.get("state", "MAIN_MENU")
    bot_response, new_state = get_response(user_message, current_state)
    session["state"] = new_state

    return jsonify({"response": bot_response})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
