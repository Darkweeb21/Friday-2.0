import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "storage" / "friday.db"

# Ensure storage folder exists
DB_PATH.parent.mkdir(exist_ok=True)


class MemoryStore:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
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

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS conversation_summary (
                session_id TEXT PRIMARY KEY,
                summary TEXT,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                confidence REAL DEFAULT 0.5,
                source TEXT,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

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

    def get_summary(self, session_id):
        cursor = self.conn.execute(
            "SELECT summary FROM conversation_summary WHERE session_id = ?",
            (session_id,)
        )
        row = cursor.fetchone()
        return row["summary"] if row else ""

    def save_summary(self, session_id, summary):
        self.conn.execute("""
            INSERT INTO conversation_summary (session_id, summary)
            VALUES (?, ?)
            ON CONFLICT(session_id)
            DO UPDATE SET summary = excluded.summary,
                          last_updated = CURRENT_TIMESTAMP
        """, (session_id, summary))
        self.conn.commit()

    def get_all_messages(self, session_id):
        cursor = self.conn.execute(
            """
            SELECT role, content, intent FROM conversations
            WHERE session_id = ?
            ORDER BY id
            """,
            (session_id,)
        )
        return cursor.fetchall()

    def delete_messages_before(self, session_id, keep_last_n):
        self.conn.execute("""
            DELETE FROM conversations
            WHERE id NOT IN (
                SELECT id FROM conversations
                WHERE session_id = ?
                ORDER BY id DESC
                LIMIT ?
            ) AND session_id = ?
        """, (session_id, keep_last_n, session_id))
        self.conn.commit()

    def save_fact(self, key, value, confidence=0.7, source="chat"):
        self.conn.execute("""
            INSERT INTO facts (key, value, confidence, source)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(key)
            DO UPDATE SET
                value = excluded.value,
                confidence = excluded.confidence,
                source = excluded.source,
                last_updated = CURRENT_TIMESTAMP
        """, (key, value, confidence, source))
        self.conn.commit()

    def get_fact(self, key):
        cursor = self.conn.execute(
            "SELECT value FROM facts WHERE key = ?",
            (key,)
        )
        row = cursor.fetchone()
        return row["value"] if row else None

    def get_all_facts(self):
        cursor = self.conn.execute(
            "SELECT key, value FROM facts ORDER BY confidence DESC"
        )
        return cursor.fetchall()
