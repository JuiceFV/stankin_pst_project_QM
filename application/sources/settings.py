from pathlib import Path
import yaml


__all__ = 'load_config'


def load_config(config_file=None):
    default_file = Path(__file__).parent.parent/'config.yaml'
    with open(default_file, 'r') as file:
        config = yaml.safe_load(file)

    cfg_dict = {}
    if config_file:
        cfg_dict = yaml.safe_load(config_file)

    config.update(**cfg_dict)

    return config
