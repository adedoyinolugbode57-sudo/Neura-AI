# main.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Optional: NLP packages
# import nltk

load_dotenv()  # Load .env variables if present

app = Flask(__name__)
CORS(app)

# Optional environment variables
DEFAULT_GENDER = os.getenv("DEFAULT_GENDER", "female")
DEFAULT_VOICE_INDEX = int(os.getenv("DEFAULT_VOICE_INDEX", 0))
DEFAULT_PITCH = float(os.getenv("DEFAULT_PITCH", 1))
DEFAULT_RATE = float(os.getenv("DEFAULT_RATE", 1))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # For online AI calls

# Health check
@app.route("/")
def home():
    return "✅ Neura-AI Backend is Running!"

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "")

    # Example AI reply (offline)
    reply_text = f"Neura-AI says: You said '{msg}' 😎"

    # Optional: add online AI logic here using OPENAI_API_KEY

    return jsonify({
        "reply": reply_text,
        "voice": {
            "gender": DEFAULT_GENDER,
            "index": DEFAULT_VOICE_INDEX,
            "pitch": DEFAULT_PITCH,
            "rate": DEFAULT_RATE
        }
    })

# Render-ready: do NOT include host/port if using Gunicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)