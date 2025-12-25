# models/summary_model.py

from models.ollama_client import OllamaClient


class SummaryModel:
    def __init__(self):
        self.client = OllamaClient()
        self.model = "mistral:latest"

    def generate(self, prompt: str) -> str:
        return self.client.generate(
            model=self.model,
            prompt=prompt
        )
