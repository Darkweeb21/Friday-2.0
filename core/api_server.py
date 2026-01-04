from fastapi import FastAPI
from pydantic import BaseModel

from models.intent_model import IntentModel
from core.router import route
from core import state

# Bootstrap application (loads all plugins)
import core.bootstrap

app = FastAPI()
intent_model = IntentModel()


# ======================================================
# 📩 COMMAND API (UNCHANGED)
# ======================================================

class CommandRequest(BaseModel):
    text: str


class CommandResponse(BaseModel):
    reply: str
    intent: str
    confidence: float
    entities: dict


@app.post("/api/command", response_model=CommandResponse)
def process_command(req: CommandRequest):
    result = intent_model.classify(req.text)
    reply = route(result, req.text)

    return {
        "reply": reply,
        "intent": result["intent"],
        "confidence": result["confidence"],
        "entities": result["entities"]
    }


# ======================================================
# 🎛️ VOICE STATE API (NEW)
# ======================================================

@app.get("/api/state")
def get_state():
    return {
        "mic_enabled": state.mic_enabled,
        "speech_enabled": state.speech_enabled,
        "is_speaking": state.is_speaking,
        "mic_temporarily_disabled": state.mic_temporarily_disabled
    }


# ======================================================
# 🎤 MICROPHONE CONTROL API (NEW)
# ======================================================

class MicRequest(BaseModel):
    enabled: bool


@app.post("/api/mic")
def set_mic(req: MicRequest):
    state.mic_enabled = req.enabled
    return {
        "success": True,
        "mic_enabled": state.mic_enabled
    }


# ======================================================
# 🔊 SPEECH (TTS) CONTROL API (NEW)
# ======================================================

class SpeechRequest(BaseModel):
    enabled: bool


@app.post("/api/speech")
def set_speech(req: SpeechRequest):
    state.speech_enabled = req.enabled
    return {
        "success": True,
        "speech_enabled": state.speech_enabled
    }

# ======================================================
# 🔁 TOGGLE MICROPHONE
# ======================================================

@app.post("/api/mic/toggle")
def toggle_mic():
    state.mic_enabled = not state.mic_enabled
    return {
        "success": True,
        "mic_enabled": state.mic_enabled
    }


# ======================================================
# 🔁 TOGGLE SPEECH (TTS)
# ======================================================

@app.post("/api/speech/toggle")
def toggle_speech():
    state.speech_enabled = not state.speech_enabled
    return {
        "success": True,
        "speech_enabled": state.speech_enabled
    }
