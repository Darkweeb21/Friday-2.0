# gives friday its personality and conersational skills

from models.ollama_client import OllamaClient

client = OllamaClient()

SYSTEM_PROMPT = (
    "You are FRIDAY, a friendly and intelligent desktop AI assistant. "
    "You can hold natural conversations, explain concepts clearly, and respond casually when needed. "
    "Be concise, helpful, and human-like."
)


def chat_response(user_input: str) -> str:
    response = client.generate(
        model="phi3:mini",
        prompt=f"{SYSTEM_PROMPT}\nUser: {user_input}\nFRIDAY:",
        temperature=0.7
    )
    return response.strip()
