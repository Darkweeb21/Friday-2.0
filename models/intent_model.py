import json
import re
from models.ollama_client import OllamaClient
from core.intents import INTENTS


class IntentModel:
    def __init__(self):
        self.client = OllamaClient()
        self.model = "phi3:mini"  # confirm via `ollama list`

        self.prompt_template = (
            "You are an intent classification engine for a desktop AI assistant named FRIDAY.\n"
            "Your task is to classify the user input into EXACTLY ONE intent from the list below.\n"
            "You must always choose the closest matching intent.\n\n"

            "INTENTS:\n"
            + "\n".join([f"- {k}: {v}" for k, v in INTENTS.items()]) +

            "\n\nEXAMPLES:\n"

            "User: open chrome\n"
            "{{ \"intent\": \"OPEN_APP\", \"confidence\": 0.95, \"entities\": {{\"app\": \"chrome\"}} }}\n\n"

            "User: open notepad\n"
            "{{ \"intent\": \"OPEN_APP\", \"confidence\": 0.95, \"entities\": {{\"app\": \"notepad\"}} }}\n\n"

            "User: increase volume\n"
            "{{ \"intent\": \"VOLUME_CONTROL\", \"confidence\": 0.90, \"entities\": {{\"action\": \"increase\"}} }}\n\n"

            "User: set volume to 30\n"
            "{{ \"intent\": \"VOLUME_CONTROL\", \"confidence\": 0.90, \"entities\": {{\"action\": \"set\", \"level\": 30}} }}\n\n"

            "User: fix this python error\n"
            "{{ \"intent\": \"CODE_HELP\", \"confidence\": 0.85, \"entities\": {{}} }}\n\n"

            "User: what is sql injection\n"
            "{{ \"intent\": \"GENERAL_CHAT\", \"confidence\": 0.80, \"entities\": {{}} }}\n\n"

            "User: gibberish command\n"
            "{{ \"intent\": \"UNKNOWN\", \"confidence\": 0.20, \"entities\": {{}} }}\n\n"

            "User: lock system\n"
            "{{ \"intent\": \"POWER_CONTROL\", \"confidence\": 0.95, \"entities\": {{\"action\": \"lock\"}} }}\n\n"

            "User: shutdown system\n"
            "{{ \"intent\": \"POWER_CONTROL\", \"confidence\": 0.95, \"entities\": {{\"action\": \"shutdown\"}} }}\n\n"

            "User: restart system\n"
            "{{ \"intent\": \"POWER_CONTROL\", \"confidence\": 0.95, \"entities\": {{\"action\": \"restart\"}} }}\n\n"
            
            
            "User: confirm\n"
            "{{ \"intent\": \"CONFIRM\", \"confidence\": 0.95, \"entities\": {{}} }}\n\n"
            
            "User: yes\n"
            "{{ \"intent\": \"CONFIRM\", \"confidence\": 0.90, \"entities\": {{}} }}\n\n"
            
            "User: cancel\n"
            "{{ \"intent\": \"CANCEL\", \"confidence\": 0.95, \"entities\": {{}} }}\n\n"
            
            "User: no\n"
            "{{ \"intent\": \"CANCEL\", \"confidence\": 0.90, \"entities\": {{}} }}\n\n"


            "RULES:\n"
            "- Output ONLY valid JSON\n"
            "- No explanations\n"
            "- confidence must be between 0 and 1\n"
            "- Extract entities when relevant (app, action, time)\n\n"

            "User input:\n"
            "{user_input}\n\n"
            "Respond ONLY with JSON:"
        )

    def _extract_json(self, text: str) -> dict:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass

        return {
            "intent": "UNKNOWN",
            "confidence": 0.0,
            "entities": {}
        }

    def classify(self, user_input: str) -> dict:
        prompt = self.prompt_template.format(user_input=user_input)

        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            temperature=0.0
        )

        return self._extract_json(response)
