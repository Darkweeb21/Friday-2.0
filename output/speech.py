import pyttsx3
from core import state

_engine = pyttsx3.init()
_engine.setProperty("rate", 175)

def speak(text: str):
    if not state.speech_enabled:
        return

    state.is_speaking = True
    try:
        _engine.say(text)
        _engine.runAndWait()
    finally:
        state.is_speaking = False


def stop_speaking():
    if state.is_speaking:
        _engine.stop()
        state.is_speaking = False
