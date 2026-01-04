from models.ollama_client import OllamaClient
import json


class FactModel:
    """
    Background fact extraction engine.

    Responsibilities:
    - Extract stable user/project facts
    - Respect explicit 'remember' requests
    - Never hallucinate or infer
    - Never break chat flow
    """

    def __init__(self, memory):
        self.memory = memory
        self.client = OllamaClient()
        self.model = "llama3:instruct"

        self.SYSTEM_PROMPT = (
            "You are a fact extraction engine for a desktop AI assistant named FRIDAY.\n\n"
            "Your job is to extract long-term facts that should be remembered.\n\n"

            "You may extract facts in TWO cases ONLY:\n"
            "1. The user explicitly states a stable fact about themselves or their project.\n"
            "2. The user explicitly asks you to remember something.\n\n"

            "STRICT RULES:\n"
            "- Do NOT infer or guess facts\n"
            "- Do NOT extract temporary states, emotions, or opinions unless the user asks to remember them\n"
            "- Do NOT extract reminders, alarms, or tasks\n"
            "- Ignore questions unless they contain an explicit memory request\n"
            "- Do NOT overwrite existing facts unless the user clearly corrects them\n\n"

            "ALLOWED FACT KEYS (use ONLY these):\n"
            "- user_name\n"
            "- user_age\n"
            "- user_birthday\n"
            "- user_location\n"
            "- user_preference\n"
            "- user_note\n"
            "- project_name\n"
            "- project_description\n"
            "- project_tech\n"
            "- project_requirement\n\n"

            "OUTPUT FORMAT:\n"
            "Return ONLY valid JSON.\n"
            "Return a JSON array of objects, each with:\n"
            "- key (string)\n"
            "- value (string)\n\n"

            "IMPORTANT:\n"
            "- If nothing should be remembered, return an empty array: []\n"
            "- Do NOT include explanations or markdown\n\n"

            "EXAMPLES:\n"
            "Input: \"My name is Himanshul\"\n"
            "Output: [{\"key\": \"user_name\", \"value\": \"Himanshul\"}]\n\n"

            "Input: \"Remember that I prefer technical explanations\"\n"
            "Output: [{\"key\": \"user_preference\", \"value\": \"Prefers technical explanations\"}]\n\n"

            "Input: \"This project uses Ollama\"\n"
            "Output: [{\"key\": \"project_tech\", \"value\": \"Ollama\"}]\n\n"

            "Input: \"Remember to call John tomorrow\"\n"
            "Output: []\n"
        )

    def extract_and_store(self, text: str):
        """
        Extract facts from user input and store them safely.
        This function must NEVER interrupt chat.
        """

        if not text or not text.strip():
            return

        text_lower = text.lower()
        explicit_memory = "remember" in text_lower

        prompt = (
            f"{self.SYSTEM_PROMPT}\n\n"
            f"Conversation text:\n{text}\n\n"
            f"Facts:"
        )

        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt
            ).strip()
        except Exception:
            return  # Ollama failure should never break chat

        # Parse JSON very defensively
        try:
            facts = json.loads(response)
            if not isinstance(facts, list):
                return
        except Exception:
            return

        for fact in facts:
            if not isinstance(fact, dict):
                continue

            key = fact.get("key")
            value = fact.get("value")

            if not key or not value:
                continue

            # preferences/notes require explicit approval
            if key in ("user_preference", "user_note") and not explicit_memory:
                continue

            # do not overwrite identical facts
            existing = self.memory.get_fact(key)
            if existing and existing == value:
                continue

            # Save fact
            try:
                self.memory.save_fact(
                    key=key,
                    value=value,
                    confidence=0.9 if explicit_memory else 0.7,
                    source="explicit" if explicit_memory else "implicit"
                )
            except Exception:
                continue  # never break chat
