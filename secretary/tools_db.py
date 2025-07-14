import os
import sqlite3
from datetime import datetime


# 每週六歸檔
def insert_into_db_archive(week_db_path: str, archive_db_path: str) -> None:
    if datetime.now().weekday() == 5:
        if os.path.exists(week_db_path):
            conn_week = sqlite3.connect(week_db_path)
            conn_archive = sqlite3.connect(archive_db_path)
            conn_archive.execute('''CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room TEXT,
                source TEXT,
                title TEXT,
                content TEXT,
                url TEXT,
                timestamp TEXT
            )''')
            for row in conn_week.execute("SELECT room, source, title, content, url, timestamp FROM messages"):
                conn_archive.execute("INSERT INTO messages (room, source, title, content, url, timestamp) VALUES (?, ?, ?, ?, ?, ?)", row)
            conn_archive.commit()
            conn_week.close()
            conn_archive.close()
            os.remove(week_db_path)

# === SQLite 更新 ===
def insert_into_db_week(week_db_path: str, items: str) -> None:
    conn = sqlite3.connect(week_db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room TEXT,
        source TEXT,
        title TEXT,
        content TEXT,
        url TEXT,
        timestamp TEXT
    )''')
    for room, sources in items.items():
        for source, entries in sources.items():
            for entry in entries:
                c.execute("INSERT INTO messages (room, source, title, content, url, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                          (room, source, entry["title"], entry["content"], entry.get("url", ""), entry["timestamp"]))
    conn.commit()
    conn.close()

