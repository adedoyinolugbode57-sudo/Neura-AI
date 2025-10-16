const chatbox = document.getElementById('chatbox');
const input = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

// Your deployed backend URL
const BASE_URL = "https://YOUR-RAILWAY-APP.up.railway.app";

// Fetch available voices
let voices = [];

function populateVoices() {
    voices = speechSynthesis.getVoices();
}

speechSynthesis.onvoiceschanged = populateVoices;

function speakText(text, gender="male") {
    if (!voices.length) populateVoices();
    
    // Filter voices by gender (simplified heuristic)
    let filteredVoices = voices.filter(v => {
        if(gender === "male") return v.name.toLowerCase().includes("male") || v.name.toLowerCase().includes("john") || v.name.toLowerCase().includes("david");
        else return v.name.toLowerCase().includes("female") || v.name.toLowerCase().includes("susan") || v.name.toLowerCase().includes("emma");
    });

    // Pick random voice from filtered list
    const voice = filteredVoices[Math.floor(Math.random() * Math.min(10, filteredVoices.length))] || voices[0];

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = voice;
    utterance.pitch = Math.random() * 0.2 + 0.9; // slight variation
    utterance.rate = Math.random() * 0.2 + 0.9;
    speechSynthesis.speak(utterance);
}

function appendMessage(sender, text) {
    const div = document.createElement('div');
    div.className = sender;
    div.textContent = `${sender.toUpperCase()}: ${text}`;
    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;

    if(sender === "ai") {
        // Randomly choose male or female voice
        const gender = Math.random() < 0.5 ? "male" : "female";
        speakText(text, gender);
    }
}

async function sendMessage() {
    const msg = input.value.trim();
    if (!msg) return;
    appendMessage('user', msg);
    input.value = '';

    try {
        const res = await fetch(`${BASE_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });
        const data = await res.json();
        appendMessage('ai', data.reply);
    } catch (err) {
        appendMessage('ai', 'Error: Cannot reach Neura-AI backend.');
        console.error(err);
    }
}

sendBtn.addEventListener('click', sendMessage);
input.addEventListener('keypress', e => { if (e.key === 'Enter') sendMessage(); });