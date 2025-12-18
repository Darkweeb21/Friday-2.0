from core.confidence import is_confident
from core.intent_registry import INTENT_REGISTRY
from core.state import confirmation_manager


def route(intent_data: dict) -> str:
    intent = intent_data.get("intent")
    confidence = intent_data.get("confidence", 0.0)
    entities = intent_data.get("entities", {})

    print(f"[DEBUG] Intent: {intent}")
    print(f"[DEBUG] Confidence: {confidence}")
    print(f"[DEBUG] Entities: {entities}")

    if not is_confident(confidence):
        return "I'm not confident about that. Can you rephrase?"

    # 🔐 Confirmation layer (handled BEFORE registry)
    if intent == "CONFIRM":
        return confirmation_manager.confirm()

    if intent == "CANCEL":
        return confirmation_manager.cancel()

    handler = INTENT_REGISTRY.get(intent)
    if not handler:
        return "I don't know how to handle that yet."

    return handler(entities)
