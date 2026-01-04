# main.py
# Bootstrap application (loads all plugins)
import core.bootstrap

from models.intent_model import IntentModel

from input.voice import VoiceInput
from input.text import TextInput
from output.console import respond
from output.speech import stop_speaking
from core import state
from core.state import confirmation_manager
from core.router import route


def safe_respond(text: str):
    """
    Speak without re-enabling mic.
    Prevents self-listening while respecting user mic choice.
    """
    state.mic_temporarily_disabled = True
    respond(text)
    state.mic_temporarily_disabled = False


def main():
    print("FRIDAY online. Debug mode enabled.")

    intent_model = IntentModel()
    voice_input = VoiceInput()
    text_input = TextInput()

    while True:
        # ================= INPUT SELECTION =================
        # 🔇 Interrupt speech if user starts interacting
        if state.is_speaking:
            stop_speaking()

        if state.mic_enabled:
            user_input = voice_input.listen()
            if not user_input:
                continue
            print(f"You (voice): {user_input}")
        else:
            user_input = text_input.listen()
            if not user_input:
                continue

        # ================= CONFIRMATION INTERCEPT =================
        if confirmation_manager.has_pending():
            normalized = user_input.lower()

            if normalized in ("yes", "y", "confirm", "ok", "sure"):
                confirmation_manager.confirm()
                safe_respond("Done.")
                continue

            if normalized in ("no", "n", "cancel", "stop"):
                result = confirmation_manager.cancel()
                safe_respond(result)
                continue

            safe_respond("Please say yes or no.")
            continue

        # ================= NORMAL FLOW =================
        intent_data = intent_model.classify(user_input)
        response = route(intent_data, user_input)

        # 🧠 UPDATE SHORT-TERM MEMORY (PART 2)
        state.last_intent = intent_data.get("intent")
        state.last_entities = intent_data.get("entities")
        state.last_action = response

        if response == "EXIT":
            safe_respond("Shutting down.")
            break

        # ================= OUTPUT =================
        safe_respond(response)


if __name__ == "__main__":
    main()
