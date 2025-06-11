from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace this with your actual Gemini API key
GEMINI_API_KEY = "AIzaSyDjdZ1apX7RhmgKz7VRCTipZAtmpv9XTNU"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_input}
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        data = response.json()

        if "candidates" in data:
            bot_response = data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            bot_response = "Error: " + data.get("error", {}).get("message", "Unknown error")

        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"response": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(debug=True)
