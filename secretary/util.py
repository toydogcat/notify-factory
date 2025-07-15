import os
import json
import logging
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler
import hydra
import feedparser
from datetime import datetime
from omegaconf import OmegaConf, DictConfig
from hydra.core.global_hydra import GlobalHydra
# import omegaconf

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    os.makedirs('logs', exist_ok=True)

    # File Output
    file_handler = RotatingFileHandler(
        'logs/running.log',
        mode='a',
        maxBytes=5 * 1024 * 1024,   # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console Output with Rich
    rich_handler = RichHandler(rich_tracebacks=True, markup=True)
    logger.addHandler(rich_handler)


def load_config() -> DictConfig:
    if not GlobalHydra.instance().is_initialized():
        hydra.initialize(
            config_path = "../configs", 
            version_base = "1.3.2"
        )
    return hydra.compose(
        config_name = "config"
    )
    
def capture_rss_info(
        ree_set: DictConfig, 
        today_data: dict
    ) -> None:
    for name, url in ree_set.items():
        feed = feedparser.parse(url)
        today_data["rooms"]["RSS"][name] = [{
            "title": entry.get("title", ""),
            "content": entry.get("summary", ""),
            "url": entry.get("link", ""),
            "timestamp": entry.get("published", datetime.now().isoformat())
        } for entry in feed.entries[:5]]

if __name__ == '__main__':
    config: DictConfig = load_config()
    config_dict: dict = OmegaConf.to_object(config)
    print(
        json.dumps(
            config_dict, 
            indent=4
        )
    )
    # print(type(config.settings.rss))
    # for name, url in config.settings.rss.items():
    #     print(name)

