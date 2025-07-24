import os
import sys
import json
import queue
import sounddevice as sd
os.environ["VOSK_LOG_LEVEL"] = "0"
# Load Config
CONFIG_PATH = "config/voice_config.json"
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH) as f:
        config = json.load(f)
else:
    config = {
        "preferred_backend": "auto",
        "whisper_model": "base",
        "vosk_model_path": "models/vosk-model-small-en-in-0.4",
        "google_language": "en-IN"
    }

# ===== VOSK =====
def listen_with_vosk():
    try:
        from vosk import Model, KaldiRecognizer
        # os.environ["VOSK_LOG_LEVEL"] = "0"
        model_path = config["vosk_model_path"]
        model = Model(model_path)
        q = queue.Queue()
        samplerate = 16000

        def callback(indata, frames, time, status):
            if status:
                print(f"⚠️ Vosk Status: {status}")
            q.put(bytes(indata))

        rec = KaldiRecognizer(model, samplerate)

        print("🎙 (Vosk) Speak now...")
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
    except Exception as e:
        print(f"❌ Vosk error: {e}")
        return None

# ===== GOOGLE STT =====
def listen_with_google():
    try:
        import speech_recognition as sr
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("🎙 (Google) Speak now...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=10, phrase_time_limit=8)

        print("🧠 Recognizing (Google)...")
        text = r.recognize_google(audio, language=config["google_language"])
        print(f"🗣 You said: {text}")
        return text
    except Exception as e:
        print(f"❌ Google STT error: {e}")
        return None

# ===== WHISPER =====
def listen_with_whisper():
    try:
        import torch
        import whisper
        import wave
        import tempfile
        import pyaudio

        print("🎙 (Whisper) Listening...")
        model = whisper.load_model(config.get("whisper_model", "base"))

        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        CHUNK = 1024
        RECORD_SECONDS = 5

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        print("🎤 Speak now (Whisper)...")
        frames = [stream.read(CHUNK) for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS))]

        stream.stop_stream()
        stream.close()
        audio.terminate()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            wf = wave.open(f.name, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            result = model.transcribe(f.name)
            os.remove(f.name)
            print(f"🗣 You said: {result['text']}")
            return result["text"]

    except Exception as e:
        print(f"❌ Whisper error: {e}")
        return None

# ===== AUTO SELECT =====
def listen_from_mic():
    backend = config.get("preferred_backend", "auto")

    # Auto fallback logic
    engines = []
    if backend == "auto":
        if sys.platform.startswith("linux"):
            engines = [listen_with_vosk, listen_with_whisper, listen_with_google]
        else:
            engines = [listen_with_google, listen_with_whisper]
    elif backend == "vosk":
        engines = [listen_with_vosk]
    elif backend == "whisper":
        engines = [listen_with_whisper]
    elif backend == "google":
        engines = [listen_with_google]
    else:
        print("❌ Invalid backend in config.")
        return ""

    for engine in engines:
        result = engine()
        if result:
            return result

    print("🤖 All voice engines failed.")
    return ""
