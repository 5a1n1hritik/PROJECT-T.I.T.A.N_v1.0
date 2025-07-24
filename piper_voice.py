from piper import PiperVoice
import sounddevice as sd
import numpy as np
import os

# Path to your ONNX model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "voices", "en_US-lessac-medium.onnx")

# Load the voice
voice = PiperVoice.load(MODEL_PATH)

# Function to speak
def speak(text: str):
    print(f"[🗣️ TTS] Speaking: {text}")

    # Correct: use .audio_int16_bytes instead of .samples
    audio_bytes = b"".join(chunk.audio_int16_bytes for chunk in voice.synthesize(text))

    # Convert bytes → float32 numpy array → normalize to [-1, 1]
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0

    # Play audio
    sd.play(audio_np, samplerate=16000)
    sd.wait()

# Example usage
if __name__ == "__main__":
    speak("Welcome to Project Titan. I am your offline assistant.")
