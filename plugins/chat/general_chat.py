from core.plugin_base import PluginBase
from models.chat_model import ChatModel
from models.fact_model import FactModel


class GeneralChatPlugin(PluginBase):
    name = "general_chat"
    intents = ["GENERAL_CHAT"]

    permission = "basic"
    requires_confirmation = False

    def execute(self, context):
        user_input = context.get("text", "").strip()

        if not user_input:
            return {
                "success": True,
                "response": "Hello! How can I help you?",
                "data": {}
            }

        llm = ChatModel()


        # FACT INGESTION (SILENT, NON-BLOCKING)

        try:
            fact_extractor = FactModel(llm.memory)
            fact_extractor.extract_and_store(user_input)
        except Exception:
            pass

        # CONTROLLED CHAT FLOW (FIXED)

        response = llm.chat([
            {
                "role": "system",
                "content": (
                    "You are FRIDAY, a concise desktop AI assistant.\n"
                    "Rules:\n"
                    "- Be brief and direct.\n"
                    "- For greetings or unclear inputs, reply in 1 short sentence.\n"
                    "- Do NOT assume the user wants technical explanations.\n"
                    "- Only give detailed answers if the user explicitly asks.\n"
                    "- Avoid storytelling, philosophy, or unrelated topics."
                )
            },
            {"role": "user", "content": user_input}
        ])

        return {
            "success": True,
            "response": response,
            "data": {}
        }
