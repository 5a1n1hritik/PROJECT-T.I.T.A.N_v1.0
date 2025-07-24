import platform
import os

# Attempt to use Piper voice model first
USE_PIPER = True

try:
    from piper import PiperVoice
    import sounddevice as sd
    import numpy as np

    # 📁 Path to Piper model
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "voices", "en_US-amy-medium.onnx")

    # 🔊 Load Piper voice model
    voice = PiperVoice.load(MODEL_PATH)
    print("✅ Piper voice loaded successfully.")
except Exception as e:
    print(f"⚠️ Piper voice load failed: {e}")
    USE_PIPER = False

# -------------------- pyttsx3 fallback --------------------

import pyttsx3

# 🛠️ Fallback TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty("volume", 1.0)
voices = engine.getProperty('voices')

def get_default_voice_index():
    system = platform.system()
    if system == "Windows":
        return 1
    elif system == "Darwin":
        return 0
    elif system == "Linux":
        return 2
    return 0

VOICE_INDEX = get_default_voice_index()
try:
    engine.setProperty('voice', voices[VOICE_INDEX].id)
except IndexError:
    print("⚠️ Invalid voice index, using default.")
    engine.setProperty('voice', voices[0].id)

# 🔍 List available pyttsx3 voices
def list_voices():
    print("🎙️ Available Voices:")
    for i, voice in enumerate(voices):
        lang = voice.languages[0].decode('utf-8') if isinstance(voice.languages[0], bytes) else voice.languages[0]
        print(f"{i}: {voice.name} ({lang}) - {voice.id}")

# 🧠 Voice switcher (optional)
def set_voice(language="en", index=None):
    selected = None
    if index is not None:
        try:
            selected = voices[index]
        except IndexError:
            print(f"⚠️ Voice index {index} not found. Using default.")
            selected = voices[get_default_voice_index()]
    else:
        for voice in voices:
            langs = [l.decode('utf-8') if isinstance(l, bytes) else l for l in voice.languages]
            if any(language in lang for lang in langs):
                selected = voice
                break
    if selected:
        engine.setProperty('voice', selected.id)
        print(f"✅ TITAN voice set to: {selected.name} ({selected.languages})")
    else:
        print("⚠️ No matching voice found. Using fallback voice.")

# 🗣️ Unified voice output function
def speak(text: str):
    print(f"[🧠 TITAN] Speaking: {text}")
    if USE_PIPER:
        try:
            # Synth and play with Piper
            audio_bytes = b"".join(chunk.audio_int16_bytes for chunk in voice.synthesize(text))
            audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            sd.play(audio_np, samplerate=22050)  # Piper sample rate for this model
            sd.wait()
        except Exception as e:
            print(f"⚠️ Piper failed: {e}. Falling back to pyttsx3.")
            engine.say(text)
            engine.runAndWait()
    else:
        try:
            engine.stop()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"⚠️ pyttsx3 error: {e}")

# ✅ Example use
# if __name__ == "__main__":
#     speak(
#         "A rainbow is a meteorological phenomenon that is caused by reflection, refraction, "
#         "and dispersion of light in water droplets resulting in a spectrum of light appearing in the sky."
#     )
