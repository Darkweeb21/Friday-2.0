import sqlite3
from core.plugin_base import PluginBase
from core.paths import DB_PATH


class AlarmsPlugin(PluginBase):
    name = "alarms"
    intents = ["SET_ALARM", "SHOW_ALARMS", "CLEAR_ALARMS"]

    permission = "basic"
    requires_confirmation = False

    def __init__(self):
        super().__init__()
        self._init_db()

    # ---------------- DB ----------------

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS alarms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trigger_time TEXT,
                label TEXT,
                active INTEGER DEFAULT 1
            )
        """)
        conn.commit()
        conn.close()

    # ---------------- ADD ----------------

    def _add_alarm(self, trigger_time, label="alarm"):
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO alarms (trigger_time, label, active) VALUES (?, ?, 1)",
            (trigger_time, label)
        )
        conn.commit()
        conn.close()

        return {
            "success": True,
            "response": f"Alarm set for {trigger_time}.",
            "data": {}
        }

    # ---------------- LIST ----------------

    def _list_alarms(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT trigger_time, label FROM alarms WHERE active = 1 ORDER BY trigger_time"
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return {
                "success": True,
                "response": "You have no active alarms.",
                "data": {}
            }

        alarms = "\n".join(f"- {t} ({l})" for t, l in rows)
        return {
            "success": True,
            "response": f"Your alarms:\n{alarms}",
            "data": {}
        }

    # ---------------- CLEAR ----------------

    def _clear_alarms(self, time=None):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if time:
            cursor.execute(
                "DELETE FROM alarms WHERE trigger_time LIKE ?",
                (f"%{time}%",)
            )
            conn.commit()
            conn.close()
            return {
                "success": True,
                "response": f"Alarm at {time} deleted.",
                "data": {}
            }

        cursor.execute("DELETE FROM alarms")
        conn.commit()
        conn.close()

        return {
            "success": True,
            "response": "All alarms cleared.",
            "data": {}
        }

    # ---------------- EXECUTE (MANDATORY) ----------------

    def execute(self, context):
        intent = context.get("intent")
        entities = context.get("entities", {})

        # SET
        if intent == "SET_ALARM":
            trigger_time = entities.get("time")
            label = entities.get("label", "alarm")

            if not trigger_time:
                return {
                    "success": False,
                    "response": "Please specify a time for the alarm.",
                    "data": {}
                }

            return self._add_alarm(trigger_time, label)

        # SHOW
        if intent == "SHOW_ALARMS":
            return self._list_alarms()

        # CLEAR
        if intent == "CLEAR_ALARMS":
            return self._clear_alarms(entities.get("time"))

        return {
            "success": False,
            "response": "Unsupported alarm action.",
            "data": {}
        }
