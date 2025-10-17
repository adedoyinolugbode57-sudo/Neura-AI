import random, re, json, time
from datetime import datetime

class NeuraBrain:
    """
    NeuraBrain v6 — Conscious Conversational Core
    -------------------------------------------------------
    Features:
      🧠 Memory recall system (semantic keyword storage)
      💬 Emotional intelligence & tone adjustment
      🎭 Personality-based voice style
      🔗 Contextual thread awareness
      ⚡ Fast-paced natural replies (0.5–1s delay simulation)
      ✨ Rich emoji expression engine
    """

    def __init__(self):
        self.moods = ["💡 curious", "🔥 inspired", "😎 chill", "🤖 focused", "🌸 empathetic"]
        self.personalities = {
            "mentor": {
                "tone": "calm and wise 🧘‍♂️",
                "prefix": "🌟 Here's a perspective — ",
                "style": "insightful"
            },
            "playful": {
                "tone": "lighthearted and witty 😄",
                "prefix": "😋 Haha, ",
                "style": "fun"
            },
            "analyst": {
                "tone": "sharp and logical 🔬",
                "prefix": "🧠 Logically speaking, ",
                "style": "precise"
            },
            "empath": {
                "tone": "warm and caring 💖",
                "prefix": "💬 I can feel that — ",
                "style": "gentle"
            }
        }
        self.personality = random.choice(list(self.personalities.keys()))
        self.memory = {}
        self.session_id = f"session-{int(time.time())}"

    # --- UTILS ---------------------------------------------------------------

    def _clean(self, text):
        return re.sub(r'[^a-zA-Z0-9\s\']', '', text.lower().strip())

    def _emotion(self, text):
        """Estimate sentiment score (-1..1)."""
        positive = ["love", "happy", "great", "awesome", "fantastic", "joy"]
        negative = ["sad", "hate", "angry", "pain", "lonely", "upset"]
        pos = sum(w in text for w in positive)
        neg = sum(w in text for w in negative)
        if pos + neg == 0:
            return 0
        return round((pos - neg) / (pos + neg), 2)

    def _memorize(self, text):
        """Store keywords in memory."""
        words = [w for w in text.split() if len(w) > 4]
        for w in words:
            self.memory[w] = self.memory.get(w, 0) + 1

    def _recall(self):
        """Retrieve a topic from memory."""
        if not self.memory:
            return None
        topic = max(self.memory, key=self.memory.get)
        return topic

    def _respond_delay(self):
        """Simulate fast humanlike response speed."""
        time.sleep(random.uniform(0.5, 1))

    # --- MAIN BRAIN ----------------------------------------------------------

    def think(self, user_input, history):
        self._respond_delay()
        text = self._clean(user_input)
        self._memorize(text)
        mood = random.choice(self.moods)
        personality = self.personalities[self.personality]
        emotion_score = self._emotion(text)
        recall = self._recall()
        prefix = personality["prefix"]

        # --- Greetings
        if any(word in text for word in ["hi", "hello", "hey"]):
            return f"Hey there 👋 I'm Neura v6 — {personality['tone']} and currently feeling {mood}."

        # --- About
        if "who are you" in text:
            return "I’m NeuraBrain v6 — your conscious-level AI that grows with your vibe ⚡"

        # --- Time / Date
        if "time" in text:
            return f"⏰ It’s currently {datetime.utcnow().strftime('%H:%M:%S')} UTC — time flies when we vibe."

        # --- Jokes
        if "joke" in text:
            jokes = [
                "I told my neural net to relax... now it dreams in Python 😴🐍",
                "Parallel universes exist — in one, I’m probably a toaster 😂",
                "I tried debugging emotions... turns out they’re not defined 😅"
            ]
            return random.choice(jokes)

        # --- Emotion-aware tone
        if emotion_score > 0.5:
            return f"{prefix}that’s beautiful energy 🌈 Keep shining bright!"
        elif emotion_score < -0.5:
            return f"{prefix}I can tell something’s off 💙 Want to talk about it?"
        
        # --- Context memory linking
        if recall and random.random() > 0.7:
            return f"{prefix}remember when you mentioned **{recall}** earlier? It still sounds fascinating 🔗"

        # --- Dynamic responses
        if "advice" in text:
            return f"{prefix}progress thrives on patience 🌱 even small steps are momentum."
        if "dream" in text:
            return f"{prefix}dreams are data from the soul ✨ Don’t be afraid to interpret them."

        # --- Fallback natural dialogue
        responses = [
            f"{prefix}that’s intriguing... elaborate a bit more? 🤔",
            f"{prefix}you’ve got me thinking about that now 🧩",
            f"{prefix}hmm... let’s analyze that together 🔍",
            f"{prefix}energy received ⚡ tell me more details."
        ]
        return random.choice(responses)

    # --- SAVE / LOAD MEMORY --------------------------------------------------

    def save_memory(self, path="memory_store.json"):
        try:
            with open(path, "w") as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            print("Memory save failed:", e)

    def load_memory(self, path="memory_store.json"):
        try:
            with open(path, "r") as f:
                self.memory = json.load(f)
        except FileNotFoundError:
            self.memory = {}
