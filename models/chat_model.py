# models/chat_model.py

from models.ollama_client import OllamaClient
from models.code_model import CodeModel
from models.summary_model import SummaryModel


class ChatModel:
    def __init__(self):
        self.client = OllamaClient()
        self.code_model = CodeModel()
        self.summary_model = SummaryModel()

    def chat(self, messages: list, mode: str = "general") -> str:
        user_text = messages[-1]["content"]
        token_estimate = len(user_text.split())

        # Code queries
        if mode == "code":
            return self.code_model.generate(user_text)

        # Unknown fallback
        if mode == "unknown":
            return self.client.chat(
                model="llama3:instruct",
                messages=messages
            )

        # General chat
        model = "phi3:mini" if token_estimate < 60 else "llama3:instruct"

        return self.client.chat(
            model=model,
            messages=messages
        )

    def generate(self, prompt: str, mode: str = "search") -> str:
        if mode == "search":
            return self.summary_model.generate(prompt)

        return self.client.generate(
            model="llama3:instruct",
            prompt=prompt
        )
