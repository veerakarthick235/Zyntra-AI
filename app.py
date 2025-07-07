from flask import Flask, render_template, request, jsonify
import requests
import os



try:
    
    from dotenv import load_dotenv
    load_dotenv()                    
except ModuleNotFoundError:
    pass




GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")      
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment")

GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    f"models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
)




app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": user_input}]}
        ]
    }

    try:
        r = requests.post(GEMINI_API_URL, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        bot_response = (
            data["candidates"][0]["content"]["parts"][0]["text"]
            if "candidates" in data else
            f"Error: {data.get('error', {}).get('message', 'Unknown error')}"
        )
    except Exception as e:
        bot_response = f"Error: {str(e)}"

    return jsonify({"response": bot_response})


if __name__ == "__main__":
    app.run(debug=True)
