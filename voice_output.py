import pyttsx3

engine = pyttsx3.init()

# Set default speaking rate
engine.setProperty('rate', 170)  # Lower = slower, more natural

# List available voices
voices = engine.getProperty('voices')

# 🎤 Voice Selector — Change index to select different voices
# On Linux, voices are often from eSpeak or Festival
VOICE_INDEX = 54  # Change to try different ones (0, 1, 2, ...)

engine.setProperty('voice', voices[VOICE_INDEX].id)


def list_voices():
    print("🎙️ Available Voices:\n")
    for i, voice in enumerate(voices):
        print(f"{i}: {voice.name} ({voice.languages}) - {voice.id}")

# 👇 Voice customization by index or language code
def set_voice(language="en", index=None):
    voices = engine.getProperty('voices')
    selected = None

    # Prioritize index if provided
    if index is not None:
        try:
            selected = voices[index]
        except IndexError:
            print(f"⚠️ Voice index {index} not found. Using default.")
    else:
        # Match by language code
        for voice in voices:
            if language in voice.languages[0].decode('utf-8'):
                selected = voice
                break

    if selected:
        engine.setProperty('voice', selected.id)
        print(f"✅ TITAN voice set to: {selected.name} ({selected.languages})")
    else:
        print("⚠️ No matching voice found. Using default voice.")

def speak(text):
    try:
        engine.stop()  # Ensure clean playback
        print(f"🤖 TITAN says: {text}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"⚠️ Voice error: {e}")
