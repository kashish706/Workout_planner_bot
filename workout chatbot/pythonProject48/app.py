from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    prompt = f"""
    Create a detailed {data['difficulty']} workout plan for:
    - Name: {data['name']}
    - Age: {data['age']}
    - Gender: {data['gender']}
    - Height: {data['height']} cm
    - Weight: {data['weight']} kg
    - Goal: {data['goal']}

    Provide a 7-day workout split with exercises and brief notes.
    """

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
    gemini_reply = response.json()

    try:
        message = gemini_reply['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        message = "Sorry, something went wrong while generating your workout plan."

    return jsonify({"response": message})

if __name__ == "__main__":
    app.run(debug=True)