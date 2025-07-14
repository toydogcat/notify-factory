from util import load_config
import os, json, sqlite3, feedparser, requests
from datetime import datetime
from encryptor import encrypt_content


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


class Puppy:
    # class property

    def __init__(self):
        # instance property
        self.config   = load_config()
        self.paths    = self.config.paths
        self.settings = self.config.settings

        self.update_today_info()
        self.update_week_info()


    def update_today_info(self):
        today_path   = self.paths.TODAY_DATA_PATH
        week_path    = self.paths.WEEK_DATA_PATH
        archive_path = self.paths.ARCHIVE_DATA_PATH

        # Load or initialize today.json
        if os.path.exists(today_path):
            with open(today_path, "r", encoding="utf-8") as f:
                self.today_data = json.load(f)
        else:
            self.today_data = {"title": "My Data Source", "updated": "", "rooms": {"RSS": {}, "Info": {}, "Weather": {}}}

        # === RSS ===
        for name, url in self.settings.get("rss", {}).items():
            feed = feedparser.parse(url)
            self.today_data["rooms"]["RSS"][name] = [{
                "title": entry.get("title", ""),
                "content": entry.get("summary", ""),
                "url": entry.get("link", ""),
                "timestamp": entry.get("published", datetime.now().isoformat())
            } for entry in feed.entries[:5]]

        # === Weather ===
        for city in self.settings.get("weather", []):
            self.today_data["rooms"]["Weather"][city] = {
                "summary": "晴時多雲",
                "temperature": "32°C",
                "timestamp": datetime.now().isoformat()
            }

        # === Info 加密（範例）===
        self.today_data["rooms"]["Info"]["PersonalNotes"] = [{
            "title": "提醒：喝水",
            "content": encrypt_content("今天要多喝水"),
            "timestamp": datetime.now().isoformat(),
            "encrypted": True
        }]

        # === 更新 today.json ===
        self.today_data["updated"] = datetime.now().isoformat()
        os.makedirs("data", exist_ok=True)
        with open(today_path, "w", encoding="utf-8") as f:
            json.dump(self.today_data, f, ensure_ascii=False, indent=2)

    def update_week_info(self):
        today_path   = self.paths.TODAY_DATA_PATH
        week_path    = self.paths.WEEK_DATA_PATH
        archive_path = self.paths.ARCHIVE_DATA_PATH
        
        # 每週六歸檔
        if datetime.now().weekday() == 5:
            if os.path.exists(week_path):
                conn_week = sqlite3.connect(week_path)
                conn_archive = sqlite3.connect(archive_path)
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
                os.remove(week_path)

        # 寫入 week.db
        insert_into_db(week_path, {"RSS": self.today_data["rooms"]["RSS"]})

if __name__ == '__main__':
    puppy = Puppy()
