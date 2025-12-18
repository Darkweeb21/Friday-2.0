import requests
import json
import time
from typing import Optional


class OllamaClient:
    """
    Lightweight client for interacting with local Ollama models.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        timeout: int = 120
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.2,
        system_prompt: Optional[str] = None,
    ) -> str:
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False,
        }

        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama request failed: {e}")

        except json.JSONDecodeError:
            raise RuntimeError("Invalid JSON response from Ollama")

