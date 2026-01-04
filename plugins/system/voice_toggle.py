from core import state

def toggle_mic(value=None):
    if value == "on":
        state.mic_enabled = True
    elif value == "off":
        state.mic_enabled = False
    else:
        state.mic_enabled = not state.mic_enabled

    return f"Microphone {'enabled' if state.mic_enabled else 'disabled'}."


def toggle_speech(value=None):
    if value == "on":
        state.speech_enabled = True
    elif value == "off":
        state.speech_enabled = False
    else:
        state.speech_enabled = not state.speech_enabled

    return f"Speech output {'enabled' if state.speech_enabled else 'disabled'}."
