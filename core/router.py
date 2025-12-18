from core.confidence import is_confident
from core.intent_registry import INTENT_REGISTRY
from core.state import confirmation_manager
import core.state as state


# Intents that MUST be confident (tasks)
TASK_INTENTS = {
    "OPEN_APP",
    "CLOSE_APP",
    "VOLUME_CONTROL",
    "SYSTEM_STATUS",
    "POWER_CONTROL",
    "SCREENSHOT",
}


def route(intent_data: dict, user_input: str) -> str:
    intent = intent_data.get("intent")
    confidence = intent_data.get("confidence", 0.0)
    entities = intent_data.get("entities", {})

    print(f"[DEBUG] Intent: {intent}")
    print(f"[DEBUG] Confidence: {confidence}")
    print(f"[DEBUG] Entities: {entities}")

    # 🔐 Confirmation layer
    if intent == "CONFIRM":
        return confirmation_manager.confirm()

    if intent == "CANCEL":
        return confirmation_manager.cancel()

    # 🔁 Context memory: repeat last action
    if intent == "REPEAT":
        if state.last_action:
            return state.last_action(state.last_entities or {})
        return "Nothing to repeat."

    # 🚫 Block LOW confidence ONLY for TASK intents
    if intent in TASK_INTENTS and not is_confident(confidence):
        return "I'm not confident about that. Can you rephrase?"

    # 🧠 Attach raw text for chat handlers
    entities["text"] = user_input

    handler = INTENT_REGISTRY.get(intent)

    # 💬 Conversational fallback
    if not handler:
        chat_handler = INTENT_REGISTRY.get("GENERAL_CHAT")
        if chat_handler:
            return chat_handler({"text": user_input})
        return "I'm not sure how to respond to that."

    response = handler(entities)

    # 🧠 Save context ONLY for real actions (not chat)
    if intent not in {"GENERAL_CHAT", "CONFIRM", "CANCEL"}:
        state.last_intent = intent
        state.last_entities = entities
        state.last_action = handler

    return response
