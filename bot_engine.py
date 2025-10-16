import random
import json
from pathlib import Path

class NeuraAIEngine:
    def __init__(self, config_file=None):
        # Load clients.json for settings
        if config_file is None:
            config_file = Path(__file__).parent / "clients.json"
        if config_file.exists():
            cfg = json.loads(config_file.read_text())
        else:
            cfg = {}
        self.fallbacks = cfg.get("fallback_responses", [
            "I'm offline right now — I can still help with general guidance.",
            "Offline: try breaking the task into smaller steps and asking me for each step.",
            "Hi — I'm Neura-AI (offline). How can I help?"
        ])
        self.default_memory = cfg.get("default_memory", 12)

    def get_response(self, text):
        """
        Generate a simple offline response.
        Can be upgraded later with NLP/ML models.
        """
        t = (text or "").lower()

        # Simple keyword matching
        if any(w in t for w in ["hello","hi","hey"]):
            return "Hi — I'm Neura-AI (offline). How can I help?"
        if "crypto" in t:
            return "Offline crypto tip: check volume and market cap. For live prices use an exchange API."
        if "weather" in t:
            return "Offline weather info: I cannot access live data now. Try local weather apps."
        if len(t.strip()) < 3:
            return "Could you give me a bit more detail?"
        
        # Random fallback
        return random.choice(self.fallbacks)

    def summarize_history(self, history):
        """
        Summarize session history (optional)
        """
        if not history:
            return "No conversation history."
        summary = []
        for item in history[-self.default_memory:]:
            role = item.get("role","user")
            content = item.get("content","")
            summary.append(f"{role}: {content}")
        return "\n".join(summary)