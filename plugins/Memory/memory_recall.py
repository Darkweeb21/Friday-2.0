from core.plugin_base import PluginBase
from core.memory import MemoryStore


class MemoryRecallPlugin(PluginBase):
    """
    Memory Recall Plugin

    Purpose:
    Provides deterministic recall of long-term user and project facts
    stored in FRIDAY's fact memory.

    Supported queries include (but are not limited to):
    - User identity (e.g., name, age, birthday)
    - Project information (e.g., project description, technologies used)
    - Generic memory recall (e.g., "What do you know about me?")

    Design principles:
    - Uses stored facts only (no inference or hallucination)
    - Deterministic responses (database-backed, not generative)
    - Safe fallback when no data is available
    - Read-only access to memory (no mutation)

    This plugin is triggered explicitly via the MEMORY_RECALL intent.
    """

    # Plugin identifier (used internally)
    name = "memory_recall"

    # Intents handled by this plugin
    intents = ["MEMORY_RECALL"]

    # Required permission level
    permission = "basic"

    # Memory recall is non-destructive and requires no confirmation
    requires_confirmation = False


    def __init__(self):
        self.memory = MemoryStore()

    def execute(self, context):
        text = context.get("text", "").lower()

        facts = self.memory.get_all_facts()
        if not facts:
            return {
                "success": True,
                "response": "I don’t have any long-term information saved about you yet.",
                "data": {}
            }

        # Convert to dict for easy lookup
        fact_map = {f["key"]: f["value"] for f in facts}

        # 🎯 Specific questions
        if "name" in text:
            name = fact_map.get("user_name")
            if name:
                return self._reply(f"Your name is {name}.")
            return self._reply("I don’t have your name saved yet.")

        if "birthday" in text:
            birthday = fact_map.get("user_birthday")
            if birthday:
                return self._reply(f"Your birthday is on {birthday}.")
            return self._reply("I don’t have your birthday saved yet.")

        if "project" in text:
            desc = fact_map.get("project_description")
            tech = fact_map.get("project_tech")

            if desc or tech:
                parts = []
                if desc:
                    parts.append(desc)
                if tech:
                    parts.append(f"It uses {tech}.")
                return self._reply(" ".join(parts))

            return self._reply("I don’t have details about your project saved yet.")

        # 🧠 Generic recall
        lines = []
        for k, v in fact_map.items():
            label = k.replace("_", " ").capitalize()
            lines.append(f"- {label}: {v}")

        return self._reply(
            "Here’s what I remember about you:\n" + "\n".join(lines)
        )

    def _reply(self, text):
        return {
            "success": True,
            "response": text,
            "data": {}
        }
