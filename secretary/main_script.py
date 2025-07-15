import logging
from util import *
from tools_db import * 
import os, json, sqlite3, feedparser, requests
from datetime import datetime
from encryptor import Master

setup_logging()

class Puppy:
    # class property
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # instance property
        self.master = Master()
        self.config   = load_config()
        self.paths    = self.config.paths
        self.settings = self.config.settings
        logging.info(f'🖥️ setup configs')

    def update_scripts(self):
        self.update_today_info()
        self.update_week_info()
        logging.info(f'🖥️ run scripts')


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
        capture_rss_info(ree_set = self.settings.rss, today_data = self.today_data)
        

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
            "content": self.master.encrypt_content("今天要多喝水"),
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
        insert_into_db_archive(week_path, archive_path)

        # 寫入 week.db
        insert_into_db_week(week_path, {"RSS": self.today_data["rooms"]["RSS"]})

if __name__ == '__main__':
    puppy = Puppy()
    puppy.update_scripts()
