# plugins/productivity/reminders.py

import sqlite3
from pathlib import Path
from core.plugin_base import PluginBase

from core.paths import DB_PATH


class RemindersPlugin(PluginBase):
    name = "reminders"
    intents = [
        "SET_REMINDER",
        "LIST_REMINDERS",
        "SHOW_REMINDERS",
        "CLEAR_REMINDERS"
    ]

    permission = "basic"
    requires_confirmation = False
    CLEAR_ACTIONS = {"clear", "delete", "remove", "reset"}
    def __init__(self):
        super().__init__()
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def execute(self, context):
        intent = context.get("intent")
        entities = context.get("entities", {})

        if intent == "SHOW_REMINDERS":
            return self._list_reminders()

        if intent == "CLEAR_REMINDERS":
            item = entities.get("item")
            return self._clear_reminders(item)

        if intent == "SET_REMINDER":
            return self._add_reminder(context)

        return {
            "success": False,
            "response": "Unsupported reminder action.",
            "data": {}
        }

    def _add_reminder(self, context):
        entities = context.get("entities", {})

        item = entities.get("item")
        action = entities.get("action")

        # Build reminder text intelligently
        if item and action:
            reminder_text = f"{action} {item}"
        elif item:
            reminder_text = item
        else:
            # fallback to raw user text
            reminder_text = context.get("text", "").strip()

        if not reminder_text:
            return {
                "success": False,
                "response": "What should I remind you about?",
                "data": {}
            }

        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO reminders (content) VALUES (?)",
            (reminder_text,)
        )
        conn.commit()
        conn.close()

        return {
            "success": True,
            "response": f"Reminder added: {reminder_text}",
            "data": {}
        }

    def _list_reminders(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute("SELECT content FROM reminders")
        reminders = [row[0] for row in cursor.fetchall()]
        conn.close()

        if not reminders:
            return {
                "success": True,
                "response": "You have no reminders.",
                "data": {}
            }

        formatted = "\n".join(f"- {r}" for r in reminders)
        return {
            "success": True,
            "response": f"Here are your reminders:\n{formatted}",
            "data": {}
        }

    def _clear_reminders(self, item=None):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        #  Delete a specific reminder
        if item:
            cursor.execute(
                "DELETE FROM reminders WHERE content LIKE ?",
                (f"%{item}%",)
            )
            conn.commit()
            conn.close()

            return {
                "success": True,
                "response": f"Reminder '{item}' deleted.",
                "data": {}
            }

        #  Delete all reminders
        cursor.execute("DELETE FROM reminders")
        conn.commit()
        conn.close()

        return {
            "success": True,
            "response": "All reminders cleared.",
            "data": {}
        }

