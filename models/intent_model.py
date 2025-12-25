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

                # ---------------- SYSTEM ----------------
                "User: open chrome\n"
                "{ \"intent\": \"OPEN_APP\", \"confidence\": 0.95, \"entities\": {\"app\": \"chrome\"} }\n\n"

                "User: open notepad\n"
                "{ \"intent\": \"OPEN_APP\", \"confidence\": 0.95, \"entities\": {\"app\": \"notepad\"} }\n\n"

                "User: increase volume\n"
                "{ \"intent\": \"VOLUME_CONTROL\", \"confidence\": 0.90, \"entities\": {\"action\": \"increase\"} }\n\n"

                "User: set volume to 30\n"
                "{ \"intent\": \"VOLUME_CONTROL\", \"confidence\": 0.90, \"entities\": {\"action\": \"set\", \"level\": 30} }\n\n"

                "User: lock system\n"
                "{ \"intent\": \"POWER_CONTROL\", \"confidence\": 0.95, \"entities\": {\"action\": \"lock\"} }\n\n"

                "User: shutdown system\n"
                "{ \"intent\": \"POWER_CONTROL\", \"confidence\": 0.95, \"entities\": {\"action\": \"shutdown\"} }\n\n"

                "User: restart system\n"
                "{ \"intent\": \"POWER_CONTROL\", \"confidence\": 0.95, \"entities\": {\"action\": \"restart\"} }\n\n"

                # ---------------- SYSTEM STATUS ----------------
                "User: cpu usage\n"
                "{ \"intent\": \"SYSTEM_STATUS\", \"confidence\": 0.95, \"entities\": {\"type\": \"cpu\"} }\n\n"

                "User: memory usage\n"
                "{ \"intent\": \"SYSTEM_STATUS\", \"confidence\": 0.95, \"entities\": {\"type\": \"memory\"} }\n\n"

                "User: battery status\n"
                "{ \"intent\": \"SYSTEM_STATUS\", \"confidence\": 0.95, \"entities\": {\"type\": \"battery\"} }\n\n"

                "User: what time is it\n"
                "{ \"intent\": \"SYSTEM_STATUS\", \"confidence\": 0.95, \"entities\": {\"type\": \"time\"} }\n\n"

                # ---------------- REMINDERS ----------------
                "User: set reminder to buy groceries\n"
                "{ \"intent\": \"SET_REMINDER\", \"confidence\": 0.95, \"entities\": {\"item\": \"buy groceries\"} }\n\n"

                "User: remind me to call mom\n"
                "{ \"intent\": \"SET_REMINDER\", \"confidence\": 0.95, \"entities\": {\"item\": \"call mom\"} }\n\n"

                "User: show reminders\n"
                "{ \"intent\": \"SHOW_REMINDERS\", \"confidence\": 0.95, \"entities\": {} }\n\n"

                "User: clear reminders\n"
                "{ \"intent\": \"CLEAR_REMINDERS\", \"confidence\": 0.95, \"entities\": {} }\n\n"

                "User: delete reminder buy groceries\n"
                "{ \"intent\": \"CLEAR_REMINDERS\", \"confidence\": 0.95, \"entities\": {\"item\": \"buy groceries\"} }\n\n"

              # ---------------- NOTES ----------------
                "User: take note buy groceries tomorrow\n"
                "{ \"intent\": \"TAKE_NOTE\", \"confidence\": 0.95, \"entities\": {\"item\": \"buy groceries tomorrow\"} }\n\n"
                
                "User: note that server IP is 10.0.0.1\n"
                "{ \"intent\": \"TAKE_NOTE\", \"confidence\": 0.95, \"entities\": {\"item\": \"server IP is 10.0.0.1\"} }\n\n"
                
                "User: add note meeting moved to friday\n"
                "{ \"intent\": \"TAKE_NOTE\", \"confidence\": 0.95, \"entities\": {\"item\": \"meeting moved to friday\"} }\n\n"
                
                "User: add note buy groceries\n"
                "{ \"intent\": \"TAKE_NOTE\", \"confidence\": 0.95, \"entities\": {\"item\": \"buy groceries\"} }\n\n"
                
                "User: save note project deadline is monday\n"
                "{ \"intent\": \"TAKE_NOTE\", \"confidence\": 0.95, \"entities\": {\"item\": \"project deadline is monday\"} }\n\n"
                
                "User: write a note server credentials\n"
                "{ \"intent\": \"TAKE_NOTE\", \"confidence\": 0.95, \"entities\": {\"item\": \"server credentials\"} }\n\n"
                
                # -------- LIST NOTES --------
                "User: show notes\n"
                "{ \"intent\": \"SHOW_NOTES\", \"confidence\": 0.95, \"entities\": {} }\n\n"
                
                "User: list my notes\n"
                "{ \"intent\": \"SHOW_NOTES\", \"confidence\": 0.95, \"entities\": {} }\n\n"
                
                "User: what are my notes\n"
                "{ \"intent\": \"SHOW_NOTES\", \"confidence\": 0.95, \"entities\": {} }\n\n"
                
                # -------- DELETE SPECIFIC NOTE --------
                "User: delete note groceries\n"
                "{ \"intent\": \"CLEAR_NOTES\", \"confidence\": 0.95, \"entities\": {\"item\": \"groceries\"} }\n\n"
                
                "User: remove note server ip\n"
                "{ \"intent\": \"CLEAR_NOTES\", \"confidence\": 0.95, \"entities\": {\"item\": \"server ip\"} }\n\n"
                
                "User: delete the meeting note\n"
                "{ \"intent\": \"CLEAR_NOTES\", \"confidence\": 0.95, \"entities\": {\"item\": \"meeting\"} }\n\n"
                
                # -------- DELETE ALL NOTES --------
                "User: clear notes\n"
                "{ \"intent\": \"CLEAR_NOTES\", \"confidence\": 0.95, \"entities\": {} }\n\n"
                
                "User: delete all notes\n"
                "{ \"intent\": \"CLEAR_NOTES\", \"confidence\": 0.95, \"entities\": {} }\n\n"
                
                "User: remove all notes\n"
                "{ \"intent\": \"CLEAR_NOTES\", \"confidence\": 0.95, \"entities\": {} }\n\n"
                
                # -------- ALARMS --------
                "User: show alarms\n"
                "{ \"intent\": \"SHOW_ALARMS\", \"confidence\": 0.95, \"entities\": {} }\n\n"
                
                "User: list my alarms\n"
                "{ \"intent\": \"SHOW_ALARMS\", \"confidence\": 0.95, \"entities\": {} }\n\n"
                
                "User: delete alarm 7 am\n"
                "{ \"intent\": \"CLEAR_ALARMS\", \"confidence\": 0.95, \"entities\": {\"time\": \"7 am\" } }\n\n"
                
                "User: remove alarm 6:30\n"
                "{ \"intent\": \"CLEAR_ALARMS\", \"confidence\": 0.95, \"entities\": {\"time\": \"6:30\"} }\n\n"
                
                "User: clear alarms\n"
                "{ \"intent\": \"CLEAR_ALARMS\", \"confidence\": 0.95, \"entities\": {} }\n\n"
                
                            # ---------------- CHAT ----------------
                "User: explain arp poisoning\n"
                "{ \"intent\": \"GENERAL_CHAT\", \"confidence\": 0.80, \"entities\": {} }\n\n"
    
                "User: write python code for port scanner\n"
                "{ \"intent\": \"GENERAL_CHAT\", \"confidence\": 0.80, \"entities\": {} }\n\n"

                # ---------------- FALLBACK ----------------
                "User: gibberish command\n"
                "{ \"intent\": \"UNKNOWN\", \"confidence\": 0.20, \"entities\": {} }\n\n"

                "RULES:\n"
                "- Output ONLY valid JSON\n"
                "- No explanations\n"
                "- confidence must be between 0 and 1\n"
                "- Extract entities when relevant (app, action, level, item)\n"
                "- If the user input contains the word \"reminder\", NEVER return UNKNOWN\n"
                "- If the user input contains the word \"note\", NEVER return UNKNOWN\n\n"

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
        prompt = self.prompt_template.replace("{user_input}", user_input)

        response = self.client.generate(
            model=self.model,
            prompt=prompt
        )

        return self._extract_json(response)
