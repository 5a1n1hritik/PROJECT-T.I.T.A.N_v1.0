import os
os.environ["VOSK_LOG_LEVEL"] = "0"  # 0 = silent, 1 = error, 2 = warning, 3 = info (default)

from t_mind import TMind
from t_core import save_memory
from voice_input import listen_from_mic
from voice_output import speak, list_voices, set_voice
from brain import ask_titan
from gpt_handler import ask_titan_gpt

def main():
    brain = TMind()
    print("🧠 TITAN is online. Say something...\n")
    print("🧠 TITAN AI Assistant Initialized.")
    print("Say something to begin...\n")
    # list_voices()
    # set_voice(language="en")  # or set_voice(index=32)

    while True:
        query = listen_from_mic()
        if query:
            response = brain.think(query)

            if response:
                speak(response)
            else:
                print("⚠️ Escalating to GPT...")
                gpt_reply = ask_titan_gpt(query)
                save_memory(query, gpt_reply)
                speak(f"[GPT] {gpt_reply}")

if __name__ == "__main__":
    main()
