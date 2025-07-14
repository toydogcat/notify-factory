import json
import hydra
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
    
if __name__ == '__main__':
    config: DictConfig = load_config()
    config_dict: dict = OmegaConf.to_object(config)
    print(
        json.dumps(
            config_dict, 
            indent=4
        )
    )

