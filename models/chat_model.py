from models.ollama_client import OllamaClient
from models.code_model import CodeModel
from models.summary_model import SummaryModel
from models.fact_model import FactModel
from core.memory import MemoryStore


class ChatModel:
    def __init__(self):
        self.client = OllamaClient()
        self.code_model = CodeModel()

        # 🧠 Memory layers
        self.memory = MemoryStore()
        self.summary_model = SummaryModel(self.memory)
        self.fact_model = FactModel(self.memory)

        self.session_id = "default"

    def chat(self, messages: list, mode: str = "general") -> str:
        # 🔧 Preserve system messages
        system_messages = [m for m in messages if m.get("role") == "system"]

        user_text = messages[-1]["content"]
        token_estimate = len(user_text.split())

        # -----------------------------
        # Store user message
        # -----------------------------
        self.memory.store(
            session_id=self.session_id,
            role="user",
            intent=None,
            content=user_text
        )

        # -----------------------------
        # 🧠 Extract FACTS (background)
        # -----------------------------
        self.fact_model.extract_and_store(user_text)

        # -----------------------------
        # Trigger summarization if needed
        # -----------------------------
        if self.summary_model.should_summarize(self.session_id):
            self.summary_model.summarize(self.session_id)

        # -----------------------------
        # Build context with memory
        # -----------------------------
        chat_messages = []
        chat_messages.extend(system_messages)

        # 🔑 Inject FACT memory as SYSTEM
        facts = self.memory.get_all_facts()
        if facts:
            facts_text = "\n".join(
                f"- {f['key']}: {f['value']}" for f in facts
            )
            chat_messages.append({
                "role": "system",
                "content": f"Known facts about the user:\n{facts_text}"
            })

        # 🧠 Inject conversation summary as SYSTEM
        summary = self.memory.get_summary(self.session_id)
        if summary and len(user_text.split()) > 3:
            chat_messages.append({
                "role": "system",
                "content": f"Conversation summary (context only):\n{summary}"
            })

        # 🔄 Inject recent conversation
        recent = self.memory.get_recent(self.session_id)
        for role, content in recent:
            chat_messages.append({
                "role": role,
                "content": content
            })

        # -----------------------------
        # Code queries
        # -----------------------------
        if mode == "code":
            response = self.code_model.generate(user_text)

        # -----------------------------
        # Unknown fallback
        # -----------------------------
        elif mode == "unknown":
            response = self.client.chat(
                model="llama3:instruct",
                messages=chat_messages
            )

        # -----------------------------
        # General chat
        # -----------------------------
        else:
            model = "phi3:mini" if token_estimate < 60 else "llama3:instruct"
            response = self.client.chat(
                model=model,
                messages=chat_messages
            )

        # -----------------------------
        # Store assistant reply
        # -----------------------------
        self.memory.store(
            session_id=self.session_id,
            role="assistant",
            intent=None,
            content=response
        )

        return response
