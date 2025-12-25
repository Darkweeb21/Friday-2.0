# models/ollama_client.py

import ollama


DEFAULT_SYSTEM_PROMPT = (
    "You are FRIDAY, a professional, concise, and helpful desktop AI assistant. "
    "You answer clearly, avoid unnecessary verbosity, and focus on being accurate. "
    "If the user greets you, respond politely. "
    "If the question is technical, explain it step by step. "
    "If you are unsure, say so honestly."
)


class OllamaClient:
    """
    Real Ollama client wrapper for FRIDAY.
    This file is the ONLY place that talks to Ollama directly.
    """

    def __init__(self, system_prompt: str | None = None):
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT

    def chat(self, model: str, messages: list) -> str:
        """
        Chat-style interaction with context.
        Automatically injects a system prompt.
        """

        # Inject system message at the beginning if not present
        if not messages or messages[0].get("role") != "system":
            messages = [{"role": "system", "content": self.system_prompt}] + messages

        response = ollama.chat(
            model=model,
            messages=messages,
            options={
                "num_ctx": 4096
            }
        )

        return response["message"]["content"]

    def generate(self, model: str, prompt: str) -> str:
        """
        Single-shot generation (used for intent classification & web summary).
        """

        full_prompt = f"{self.system_prompt}\n\n{prompt}"

        response = ollama.generate(
            model=model,
            prompt=full_prompt,
            options={
                "num_ctx": 4096
            }
        )

        return response["response"]
