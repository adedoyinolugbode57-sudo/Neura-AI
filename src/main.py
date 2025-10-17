# src/main.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import json, random, time, os
from datetime import datetime
from bot_engine import NeuraBrain

app = Flask(__name__)
CORS(app)

# Initialize AI brain
brain = NeuraBrain()

# === MEMORY FILES ===
MEMORY_FILE = "src/memory_store.json"
LOG_FILE = "src/chat_logs.json"

# === Utility Functions ===
def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def log_conversation(user, ai, emotion):
    logs = load_json(LOG_FILE, [])
    logs.append({
        "user": user,
        "ai": ai,
        "emotion": emotion,
        "timestamp": datetime.now().isoformat()
    })
    save_json(LOG_FILE, logs)

# === ROUTES ===
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Neura-AI Online ✅",
        "message": "Welcome to Neura-AI v2.5 — Skyrocketed Intelligence 💥"
    })

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    user_emotion = data.get("emotion", "neutral")

    if not user_message:
        return jsonify({"response": "🤔 I didn’t catch that! Can you rephrase?"}), 400

    # Generate reply
    start = time.time()
    ai_reply = brain.respond(user_message, user_emotion)
    duration = round(time.time() - start, 2)

    # Add emojis and expressions based on mood
    if user_emotion == "happy":
        ai_reply += " 😄✨"
    elif user_emotion == "sad":
        ai_reply += " 💙🤗"
    elif user_emotion == "angry":
        ai_reply += " 😤🔥"
    else:
        ai_reply += " 😊"

    log_conversation(user_message, ai_reply, user_emotion)

    return jsonify({
        "response": ai_reply,
        "processing_time": f"{duration}s"
    })

@app.route("/memory", methods=["GET"])
def memory_status():
    memory = load_json(MEMORY_FILE, {})
    return jsonify({"memory": memory})

@app.route("/memory", methods=["POST"])
def memory_update():
    data = request.get_json()
    memory = load_json(MEMORY_FILE, {})
    memory.update(data)
    save_json(MEMORY_FILE, memory)
    return jsonify({"message": "🧠 Memory updated successfully!"})

# === RUN ===
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
