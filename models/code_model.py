# models/code_model.py

from models.ollama_client import OllamaClient


class CodeModel:
    def __init__(self):
        self.client = OllamaClient()
        self.model = "deepseek-coder:latest"

    def generate(self, prompt: str) -> str:
        return self.client.generate(
            model=self.model,
            prompt=prompt
        )
