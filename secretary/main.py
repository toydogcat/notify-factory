import os, json, sqlite3, feedparser, requests
from datetime import datetime
from encryptor import encrypt_content

CONFIG_PATH = "configs/config.json"

# Load config
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

# Load or initialize today.json
today_path = "data/today.json"
if os.path.exists(today_path):
    with open(today_path, "r", encoding="utf-8") as f:
        today_data = json.load(f)
else:
    today_data = {"title": "My Data Source", "updated": "", "rooms": {"RSS": {}, "Info": {}, "Weather": {}}}

# === RSS ===
for name, url in config.get("rss", {}).items():
    feed = feedparser.parse(url)
    today_data["rooms"]["RSS"][name] = [{
        "title": entry.get("title", ""),
        "content": entry.get("summary", ""),
        "url": entry.get("link", ""),
        "timestamp": entry.get("published", datetime.now().isoformat())
    } for entry in feed.entries[:5]]

# === Weather ===
for city in config.get("weather", []):
    today_data["rooms"]["Weather"][city] = {
        "summary": "晴時多雲",
        "temperature": "32°C",
        "timestamp": datetime.now().isoformat()
    }

# === Info 加密（範例）===
today_data["rooms"]["Info"]["PersonalNotes"] = [{
    "title": "提醒：喝水",
    "content": encrypt_content("今天要多喝水"),
    "timestamp": datetime.now().isoformat(),
    "encrypted": True
}]

# === 更新 today.json ===
today_data["updated"] = datetime.now().isoformat()
os.makedirs("data", exist_ok=True)
with open(today_path, "w", encoding="utf-8") as f:
    json.dump(today_data, f, ensure_ascii=False, indent=2)

# === SQLite 更新 ===
def insert_into_db(db_path, items):
    conn = sqlite3.connect(db_path)
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

# 每週六歸檔
if datetime.now().weekday() == 5:
    if os.path.exists("data/week.db"):
        conn_week = sqlite3.connect("data/week.db")
        conn_archive = sqlite3.connect("data/archive.db")
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
        os.remove("data/week.db")

# 寫入 week.db
insert_into_db("data/week.db", {"RSS": today_data["rooms"]["RSS"]})
