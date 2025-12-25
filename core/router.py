from core.confidence import is_confident
from core.state import confirmation_manager, SESSION_ID
import core.state as state
from core.memory import MemoryStore
from core.plugin_registry import PLUGIN_REGISTRY

memory_store = MemoryStore()

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

    # 🔁 Repeat last action
    if intent == "REPEAT":
        if state.last_action:
            result = state.last_action.execute({
                "text": user_input,
                "intent": state.last_intent,
                "entities": state.last_entities or {},
            })
            return result.get("response", "Failed to repeat last action.")
        return "Nothing to repeat."

    # 🚫 Confidence gate for task intents
    if intent in TASK_INTENTS and not is_confident(confidence):
        return "I'm not confident about that. Can you rephrase?"

    # 🧠 Plugin context
    context = {
        "text": user_input,
        "intent": intent,
        "entities": entities,
        "confidence": confidence,
    }

    # 🔌 Resolve plugin
    # Treat UNKNOWN as GENERAL_CHAT
    if intent == "UNKNOWN":
        intent = "GENERAL_CHAT"

    plugin_cls = PLUGIN_REGISTRY.get(intent) or PLUGIN_REGISTRY.get("GENERAL_CHAT")

    if not plugin_cls:
        return "I'm not sure how to respond to that."

    plugin = plugin_cls()
    result = plugin.execute(context)
    response = result.get("response", "Something went wrong.")

    # 💾 Persist conversation
    memory_store.store(SESSION_ID, "user", intent, user_input)
    memory_store.store(SESSION_ID, "assistant", intent, response)

    # 🧠 Save last action (non-chat)
    if intent not in {"GENERAL_CHAT", "CONFIRM", "CANCEL"}:
        state.last_intent = intent
        state.last_entities = entities
        state.last_action = plugin

    # 🧠 RAM chat memory
    if intent in {"GENERAL_CHAT", "UNKNOWN"}:
        state.chat_history.append({"role": "user", "content": user_input})
        state.chat_history.append({"role": "assistant", "content": response})
        state.chat_history = state.chat_history[-state.CHAT_MEMORY_LIMIT:]

    return response
