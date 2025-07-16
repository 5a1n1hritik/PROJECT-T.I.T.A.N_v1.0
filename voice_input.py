# import speech_recognition as sr
#
#
# def listen_from_mic():
#     r = sr.Recognizer()
#
#     mic_name = "pulse"  # or try "pulse"
#     mic_index = sr.Microphone.list_microphone_names().index(mic_name)
#
#     with sr.Microphone(device_index=mic_index) as source:
#         print(f"🎙 Using mic: {mic_name}")
#         r.adjust_for_ambient_noise(source, duration=1)
#         print("🎙 Speak now...")
#         audio = r.listen(source, timeout=10, phrase_time_limit=8)
#
#     try:
#         print("🧠 Recognizing...")
#         text = r.recognize_google(audio, language="en-IN")
#         print(f"🗣 You said: {text}")
#         return text
#     except sr.UnknownValueError:
#         print("🤖 I couldn't understand.")
#     except sr.RequestError as e:
#         print(f"🔌 API error: {e}")
#     except Exception as e:
#         print(f"❌ Other error: {e}")
#
#     return ""

import os
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

os.environ["VOSK_LOG_LEVEL"] = "0"

q = queue.Queue()
samplerate = 16000
model = Model("models/vosk-model-small-en-in-0.4")


def callback(indata, frames, time, status):
    if status:
        print(f"⚠️ Status: {status}")
    q.put(bytes(indata))


def listen_from_mic():
    print("🎙 Speak now...")

    # Set default input device if needed:
    # sd.default.device = 5  # optional

    rec = KaldiRecognizer(model, samplerate)

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text.strip():
                    print(f"🗣 You said: {text}")
                    return text
                else:
                    print("🤖 Didn't catch that, try again.")
                    return ""
