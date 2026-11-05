import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "nexus_history.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            module TEXT NOT NULL,
            details TEXT NOT NULL
        )""")

def add_log(module: str, details: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO activity (created_at, module, details) VALUES (?, ?, ?)",
            (datetime.now().astimezone().isoformat(timespec="seconds"), module, details)
        )

def get_logs(limit=100):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            "SELECT created_at, module, details FROM activity ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
