# t_mind.py
from t_core import recall_memory, save_memory
from datetime import datetime

# Basic rules-based internal decision engine
class TMind:
    def __init__(self):
        self.name = "TITAN"
        self.version = "v1.0"
        self.rules = {
            "hello": "Hi, I am TITAN. How can I help you today?",
            "hi": "Hi, I am TITAN. How can I help you today?",
            "your name": "I am your A.I assistant, TITAN.",
            "who created you": "I was created by Hritik Saini, a passionate developer.",
            "how are you": "I'm operational and ready, Commander.",
            "status": "All systems nominal. No alerts in memory.",
            "remind me": "Noted. Storing your reminder in core memory.",
            "shutdown": "Initiating safe shutdown. Awaiting final confirmation.",
            "what can you do": "I can listen, speak, and help you with various tasks. Try saying something!",
            "bye": "Goodbye! It was nice talking to you.",
            "exit": "Goodbye! It was nice talking to you.",
            "quit": "Goodbye! It was nice talking to you."
        }

    def think(self, user_input: str):
        query = user_input.lower().strip()

        # Memory recall
        memory_response = recall_memory(query)
        if memory_response:
            return f"[Memory Recall] {memory_response}"

        # Time/date handling
        if "time" in query:
            now = datetime.now().strftime("%I:%M %p")
            return f"The current time is {now}."
        if "date" in query:
            today = datetime.now().strftime("%A, %d %B %Y")
            return f"Today is {today}."

        # Rule matching
        for trigger, response in self.rules.items():
            if trigger in query:
                save_memory(query, response)
                return f"[Internal Logic] {response}"

        # No match
        return None
