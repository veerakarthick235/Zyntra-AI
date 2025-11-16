from flask import Flask, render_template, request, jsonify, Response
import google.generativeai as genai
import os
import json
import time

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash')

app = Flask(__name__)

# Session-based chat storage (use Redis/DB in production)
chat_sessions = {}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    session_id = request.json.get("session_id", "default")
    
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    chat_history = chat_sessions[session_id]
    
    # Store user message
    chat_history.append({"role": "user", "text": user_input})

    # Check creator question
    lower = user_input.lower()
    if any(word in lower for word in ["who created", "who built", "developer", "creator", "who made"]):
        bot_msg = (
            "🚀 I was created by **Veera Karthick**, an AI Engineer, "
            "Gen AI Developer, and LLM Expert specializing in cutting-edge AI solutions."
        )
        chat_history.append({"role": "model", "text": bot_msg})
        return jsonify({"response": bot_msg})

    # Build conversation for Gemini
    formatted_history = [
        {"role": msg["role"], "parts": [{"text": msg["text"]}]} 
        for msg in chat_history
    ]

    try:
        response = model.generate_content(formatted_history)
        full_text = response.text
        chat_history.append({"role": "model", "text": full_text})
        
        return jsonify({"response": full_text})

    except Exception as e:
        error_msg = f"⚠️ Error: {str(e)}"
        return jsonify({"response": error_msg}), 500


@app.route("/clear", methods=["POST"])
def clear_chat():
    session_id = request.json.get("session_id", "default")
    if session_id in chat_sessions:
        chat_sessions[session_id] = []
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(debug=True)
