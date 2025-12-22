import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "storage" / "friday.db"

# Ensure storage folder exists
DB_PATH.parent.mkdir(exist_ok=True)


class MemoryStore:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT,
                role TEXT,
                intent TEXT,
                content TEXT
            )
        """)
        self.conn.commit()

    def store(self, session_id, role, intent, content):
        self.conn.execute(
            "INSERT INTO conversations (session_id, role, intent, content) VALUES (?, ?, ?, ?)",
            (session_id, role, intent, content)
        )
        self.conn.commit()

    def get_recent(self, session_id, limit=6):
        cursor = self.conn.execute(
            """
            SELECT role, content FROM conversations
            WHERE session_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (session_id, limit)
        )
        return list(reversed(cursor.fetchall()))
    def get_recent_global(self, limit=6):
        cursor = self.conn.execute(
            """
            SELECT role, content FROM conversations
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )
        return list(reversed(cursor.fetchall()))


    def get_app_mapping(self, app_name: str, mode: str):
        """
        mode: 'open' or 'close'
        """
        key = app_name.lower()
        cursor = self.conn.execute(
            """
            SELECT content FROM conversations
            WHERE intent = 'APP_MAPPING'
              AND session_id = 'GLOBAL'
              AND content LIKE ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (f"{mode}|{key}|%",)
        )
        row = cursor.fetchone()
        if not row:
            return None
        return row[0].split("|", 2)[2]

    def save_app_mapping(self, app_name: str, value: str, mode: str):
        key = app_name.lower()
        content = f"{mode}|{key}|{value}"
        self.store(
            session_id="GLOBAL",
            role="system",
            intent="APP_MAPPING",
            content=content
        )
