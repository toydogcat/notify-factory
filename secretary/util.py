import json
import hydra
import feedparser
from datetime import datetime
from omegaconf import OmegaConf, DictConfig
# import omegaconf

def load_config() -> DictConfig:
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

