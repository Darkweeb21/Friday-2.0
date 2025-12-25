from core.plugin_base import PluginBase
from models.chat_model import ChatModel
import core.state as state

from plugins.web.router import needs_web_search
from plugins.web.search import web_search
from plugins.web.summarize import summarize_web_results


class GeneralChatPlugin(PluginBase):
    name = "general_chat"
    intents = ["GENERAL_CHAT"]

    permission = "basic"
    requires_confirmation = False

    def execute(self, context):
        user_input = context.get("text", "").strip()
        confidence = context.get("confidence", 0.0)

        if not user_input:
            return {
                "success": True,
                "response": "Hello! How can I help you?",
                "data": {}
            }

        llm = ChatModel()

        # 🌐 Web fallback
        if needs_web_search(user_input, confidence):
            results = web_search(user_input)
            response = summarize_web_results(user_input, results, llm)

        # 🧠 Normal conversation
        else:
            messages = state.chat_history + [
                {"role": "user", "content": user_input}
            ]
            response = llm.chat(messages)

        return {
            "success": True,
            "response": response,
            "data": {}
        }
