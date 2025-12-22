# plugins/chat/general_chat.py

from core.plugin_base import PluginBase


class GeneralChatPlugin(PluginBase):
    name = "general_chat"
    intents = ["GENERAL_CHAT"]

    permission = "basic"
    requires_confirmation = False

    def execute(self, context):
        text = context.get("text", "").strip()

        if not text:
            return {
                "success": True,
                "response": "Hello! How can I help you?",
                "data": {}
            }

        return {
            "success": True,
            "response": "I’m here. What would you like to do?",
            "data": {}
        }
