from models.ollama_client import OllamaClient


class SummaryModel:
    def __init__(self, memory):
        self.memory = memory
        self.client = OllamaClient()
        self.model = "llama3:instruct"

        self.SYSTEM_PROMPT = (
            "You are a memory summarization engine for a desktop AI assistant named FRIDAY.\n\n"
            "Summarize the conversation into a concise factual memory preserving:\n"
            "- User goals and preferences\n"
            "- Ongoing tasks or projects\n"
            "- Important decisions or conclusions\n"
            "- Technical context (tools, code, errors, architecture)\n\n"
            "Rules:\n"
            "- No greetings or filler\n"
            "- No assumptions\n"
            "- Third person only\n"
            "- Under 120 words\n"
        )

    def should_summarize(self, session_id, threshold=12):
        messages = self.memory.get_all_messages(session_id)
        chat_count = sum(
            1 for m in messages
            if m["intent"] in ("GENERAL_CHAT", "UNKNOWN", None)
        )
        return chat_count >= threshold

    def summarize(self, session_id, keep_last_n=6):
        messages = self.memory.get_all_messages(session_id)

        #  ONLY summarize chat-related intents
        chat_messages = [
            m for m in messages
            if m["intent"] in ("GENERAL_CHAT", "UNKNOWN", None)
        ]

        if len(chat_messages) <= keep_last_n:
            return

        old_messages = chat_messages[:-keep_last_n]
        existing_summary = self.memory.get_summary(session_id)

        conversation_text = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}"
            for m in old_messages
        )

        prompt = (
            f"{self.SYSTEM_PROMPT}\n\n"
            f"Existing summary:\n{existing_summary or 'None'}\n\n"
            f"Conversation messages:\n{conversation_text}\n\n"
            f"Updated summary:"
        )

        summary = self.client.generate(
            model=self.model,
            prompt=prompt
        ).strip()

        self.memory.save_summary(session_id, summary)

        # ✅ Delete ONLY summarized chat messages
        self.memory.delete_messages_before(session_id, keep_last_n)

