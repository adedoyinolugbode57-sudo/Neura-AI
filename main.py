from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, json, datetime
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Flask app
app = Flask(__name__, static_folder="frontend")
CORS(app)

# Paths
CLIENTS_FILE = "clients.json"
CHAT_LOGS_FILE = "chat_logs.json"
MEMORY_FILE = "memory_store.json"

# Load clients
if os.path.exists(CLIENTS_FILE):
    with open(CLIENTS_FILE, "r") as f:
        clients = json.load(f)
else:
    clients = {"clients": []}

# Load memory
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory_store = json.load(f)
else:
    memory_store = {}

# Load chat logs
if os.path.exists(CHAT_LOGS_FILE):
    with open(CHAT_LOGS_FILE, "r") as f:
        chat_logs = json.load(f)
else:
    chat_logs = []

# ---------- Utility Functions ----------
def log_chat(client_id, role, message):
    timestamp = datetime.datetime.now().isoformat()
    chat_logs.append({"client": client_id, "role": role, "message": message, "time": timestamp})
    with open(CHAT_LOGS_FILE, "w") as f:
        json.dump(chat_logs, f, indent=4)

def update_memory(client_id, message):
    if client_id not in memory_store:
        memory_store[client_id] = []
    memory_store[client_id].append(message)
    # Limit memory to last 10 messages
    memory_store[client_id] = memory_store[client_id][-10:]
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_store, f, indent=4)

def get_client(client_id):
    for c in clients.get("clients", []):
        if c["id"] == client_id:
            return c
    return None

# ---------- Routes ----------
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    client_id = data.get("client_id", "guest")
    message = data.get("message", "")

    # Log user message
    log_chat(client_id, "user", message)
    update_memory(client_id, message)

    # ---------- Offline responses ----------
    offline_responses = [
        "I’m thinking about that 🤔",
        "Interesting question!",
        "Could you clarify a bit?",
        "That sounds exciting 😎",
        "I’ll remember that."
    ]
    
    # ---------- Online responses placeholder ----------
    # Here you can integrate OpenAI or other APIs
    online_response = f"Neura-AI says: You said '{message}' 😎"

    # Decide randomly whether to reply online or offline
    reply = random.choice([online_response] + offline_responses)

    # Log AI reply
    log_chat(client_id, "ai", reply)
    update_memory(client_id, reply)

    return jsonify({"reply": reply})

@app.route('/chat_logs', methods=['GET'])
def get_logs():
    return jsonify(chat_logs)

@app.route('/memory/<client_id>', methods=['GET'])
def get_memory(client_id):
    return jsonify(memory_store.get(client_id, []))

# ---------- Run Server ----------
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)