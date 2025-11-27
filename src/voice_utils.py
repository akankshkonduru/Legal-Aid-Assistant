import os
import sys
import json
import torch
import numpy as np
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# ---------------------------------------------------------
# Make root directory importable
# ---------------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

# ---------------------------------------------------------
# Import your full LangChain RAG + LLaMA bot
# ---------------------------------------------------------
from src.combined_chain import CombinedLegalChatbot


# ---------------------------------------------------------
# 1. Load Vosk STT (Offline, Free)
# ---------------------------------------------------------
VOSK_MODEL_PATH = os.path.join(ROOT_DIR, "models", "vosk-model-small-en-in-0.4")

if not os.path.exists(VOSK_MODEL_PATH):
    raise FileNotFoundError(
        f"Vosk model not found at {VOSK_MODEL_PATH}.\n"
        "Download from: https://alphacephei.com/vosk/models"
    )

print("🎤 Loading Vosk STT Model...")
vosk_model = Model(VOSK_MODEL_PATH)
rec = KaldiRecognizer(vosk_model, 16000)


# ---------------------------------------------------------
# 2. Load Silero TTS (Offline, Free) — Windows Safe
# ---------------------------------------------------------
TTS_PATH = os.path.join(ROOT_DIR, "silero_tts.pt")

if not os.path.exists(TTS_PATH):
    print("⬇️ Downloading Silero TTS model...")
    import urllib.request
    urllib.request.urlretrieve(
        "https://models.silero.ai/models/tts/en/v3_en.pt",
        TTS_PATH
    )
    print("✔ Silero TTS downloaded!")

print("🔊 Loading Silero TTS model...")
silero_model = torch.jit.load(TTS_PATH, map_location="cpu")
silero_model.eval()

def tts(text):
    """Speak text using Silero TTS."""
    audio = silero_model.apply_tts(text=text)
    audio = torch.tensor(audio, dtype=torch.float32).numpy()
    sd.play(audio, 48000)
    sd.wait()


# ---------------------------------------------------------
# 3. Initialize Your RAG + LLaMA Bot
# ---------------------------------------------------------
print("🤖 Initializing Legal RAG Bot...")
bot = CombinedLegalChatbot(model_name="llama2")

def rag_llama_chat(query):
    """Wrapper to call your full RAG chatbot."""
    try:
        return bot.generate(query)
    except Exception as e:
        print("❌ RAG Error:", e)
        return "I encountered an issue processing your request."


# ---------------------------------------------------------
# 4. Voice Callback — Real-Time STT → RAG → TTS
# ---------------------------------------------------------
def callback(indata, frames, time, status):
    data = indata.tobytes()

    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        text = result.get("text", "").strip()

        if text:
            print(f"\n🧑 You: {text}")

            # Process using RAG + LLaMA
            reply = rag_llama_chat(text)
            print(f"🤖 Bot: {reply}")

            # Speak it
            tts(reply)


# ---------------------------------------------------------
# 5. Start Real-Time Streaming Voice Assistant
# ---------------------------------------------------------
def start_voice():
    print("\n🎧 Listening... Speak into your microphone.")
    print("Press CTRL + C to exit.\n")

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback
    ):
        while True:
            sd.sleep(1000)


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------
if __name__ == "__main__":
    start_voice()
