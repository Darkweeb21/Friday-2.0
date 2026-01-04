import sqlite3
from core.plugin_base import PluginBase
from core.paths import DB_PATH


class NotesPlugin(PluginBase):
    name = "notes"
    intents = ["TAKE_NOTE", "SHOW_NOTES", "CLEAR_NOTES"]

    permission = "basic"
    requires_confirmation = False

    def __init__(self):
        super().__init__()
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT
            )
        """)
        conn.commit()
        conn.close()

    def _add_note(self, content):
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO notes (content) VALUES (?)",
            (content,)
        )
        conn.commit()
        conn.close()

        return {
            "success": True,
            "response": f"Note added: {content}",
            "data": {}
        }

    def _list_notes(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM notes")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return {
                "success": True,
                "response": "You have no notes.",
                "data": {}
            }

        notes = "\n".join(f"- {r[0]}" for r in rows)
        return {
            "success": True,
            "response": f"Here are your notes:\n{notes}",
            "data": {}
        }

    def _clear_notes(self, item=None):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if item:
            cursor.execute(
                "DELETE FROM notes WHERE content LIKE ?",
                (f"%{item}%",)
            )
            conn.commit()
            conn.close()
            return {
                "success": True,
                "response": f"Note '{item}' deleted.",
                "data": {}
            }

        cursor.execute("DELETE FROM notes")
        conn.commit()
        conn.close()
        return {
            "success": True,
            "response": "All notes cleared.",
            "data": {}
        }

    #  THIS METHOD IS MANDATORY
    def execute(self, context):
        intent = context.get("intent")
        entities = context.get("entities", {})
        text = context.get("text", "")

        if intent == "TAKE_NOTE":
            content = entities.get("item") or text
            return self._add_note(content)

        if intent == "SHOW_NOTES":
            return self._list_notes()

        import sqlite3
        from core.plugin_base import PluginBase
        from core.paths import DB_PATH

        class NotesPlugin(PluginBase):
            name = "notes"
            intents = ["TAKE_NOTE", "SHOW_NOTES", "CLEAR_NOTES"]

            permission = "basic"
            requires_confirmation = False

            def __init__(self):
                super().__init__()
                self._init_db()

            def _init_db(self):
                conn = sqlite3.connect(DB_PATH)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT
                    )
                """)
                conn.commit()
                conn.close()

            def _add_note(self, content):
                conn = sqlite3.connect(DB_PATH)
                conn.execute(
                    "INSERT INTO notes (content) VALUES (?)",
                    (content,)
                )
                conn.commit()
                conn.close()

                return {
                    "success": True,
                    "response": f"Note added: {content}",
                    "data": {}
                }

            def _list_notes(self):
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT content FROM notes")
                rows = cursor.fetchall()
                conn.close()

                if not rows:
                    return {
                        "success": True,
                        "response": "You have no notes.",
                        "data": {}
                    }

                notes = "\n".join(f"- {r[0]}" for r in rows)
                return {
                    "success": True,
                    "response": f"Here are your notes:\n{notes}",
                    "data": {}
                }

            def _clear_notes(self, item=None):
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()

                if item:
                    cursor.execute(
                        "DELETE FROM notes WHERE content LIKE ?",
                        (f"%{item}%",)
                    )
                    conn.commit()
                    conn.close()
                    return {
                        "success": True,
                        "response": f"Note '{item}' deleted.",
                        "data": {}
                    }

                cursor.execute("DELETE FROM notes")
                conn.commit()
                conn.close()
                return {
                    "success": True,
                    "response": "All notes cleared.",
                    "data": {}
                }

            #  THIS METHOD IS MANDATORY
            def execute(self, context):
                intent = context.get("intent")
                entities = context.get("entities", {})
                text = context.get("text", "")

                if intent == "TAKE_NOTE":
                    content = entities.get("item") or text
                    return self._add_note(content)

                if intent == "SHOW_NOTES":
                    return self._list_notes()

                if intent == "CLEAR_NOTES":
                    return self._clear_notes(entities.get("item"))

                return {
                    "success": False,
                    "response": "Unsupported notes action.",
                    "data": {}
                }

        return {
            "success": False,
            "response": "Unsupported notes action.",
            "data": {}
        }
