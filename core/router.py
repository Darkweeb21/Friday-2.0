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


def is_question(text: str) -> bool:
    """
    Generic question detector.
    MEMORY_RECALL must ONLY trigger on questions.
    """
    question_starters = (
        "what", "when", "who", "where", "why", "how",
        "do i", "am i", "is my", "tell me", "show me",
    )
    return (
        "?" in text
        or any(text.startswith(q) for q in question_starters)
    )


def route(intent_data: dict, user_input: str) -> str:
    intent = intent_data.get("intent")
    confidence = intent_data.get("confidence", 0.0)
    entities = intent_data.get("entities", {})

    print(f"[DEBUG] Intent: {intent}")
    print(f"[DEBUG] Confidence: {confidence}")
    print(f"[DEBUG] Entities: {entities}")

    text_lower = user_input.lower().strip()

    # =========================================================
    # 🧠 MEMORY RECALL — QUESTIONS ONLY (GENERIC)
    # =========================================================
    # =========================================================
    # 🧠 MEMORY RECALL — ANY PERSONAL QUESTION
    # =========================================================
    if is_question(text_lower):
        personal_markers = ("my ", "me ", "about me", "it ")

        if any(p in text_lower for p in personal_markers):
            intent = "MEMORY_RECALL"

    # =========================================================
    # 🧠 FACT INGESTION — STATEMENTS NEVER TRIGGER RECALL
    # =========================================================
    if not is_question(text_lower):
        if intent == "MEMORY_RECALL":
            intent = "GENERAL_CHAT"

    # =========================================================
    # 🔐 CONFIRMATION LAYER
    # =========================================================
    if intent == "CONFIRM":
        return confirmation_manager.confirm()

    if intent == "CANCEL":
        return confirmation_manager.cancel()

    # =========================================================
    # 🔁 REPEAT LAST ACTION
    # =========================================================
    if intent == "REPEAT":
        if state.last_action:
            result = state.last_action.execute({
                "text": user_input,
                "intent": state.last_intent,
                "entities": state.last_entities or {},
            })
            return result.get("response", "Failed to repeat last action.")
        return "Nothing to repeat."

    # =========================================================
    # 🚫 CONFIDENCE GATE FOR TASK INTENTS
    # =========================================================
    if intent in TASK_INTENTS and not is_confident(confidence):
        return "I'm not confident about that. Can you rephrase?"

    # =========================================================
    # 🧠 PLUGIN CONTEXT
    # =========================================================
    context = {
        "text": user_input,
        "intent": intent,
        "entities": entities,
        "confidence": confidence,
    }

    # =========================================================
    # 🔌 PLUGIN RESOLUTION
    # =========================================================
    if intent == "UNKNOWN" and intent != "MEMORY_RECALL":
        intent = "GENERAL_CHAT"

    plugin_cls = PLUGIN_REGISTRY.get(intent) or PLUGIN_REGISTRY.get("GENERAL_CHAT")

    if not plugin_cls:
        return "I'm not sure how to respond to that."

    plugin = plugin_cls()
    result = plugin.execute(context)
    response = result.get("response", "Something went wrong.")

    # =========================================================
    # 💾 PERSIST CONVERSATION
    # =========================================================
    memory_store.store(SESSION_ID, "user", intent, user_input)
    memory_store.store(SESSION_ID, "assistant", intent, response)

    # =========================================================
    # 🧠 SAVE LAST ACTION (NON-CHAT)
    # =========================================================
    if intent not in {"GENERAL_CHAT", "CONFIRM", "CANCEL", "MEMORY_RECALL"}:
        state.last_intent = intent
        state.last_entities = entities
        state.last_action = plugin

    return response
