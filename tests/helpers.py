import sys
import importlib

import yaml


CONFIG_PATH = "app.config"


def reload_config_module():
    if CONFIG_PATH in sys.modules:
        del sys.modules[CONFIG_PATH]
        
    cfg_mod = importlib.import_module(CONFIG_PATH)

    return cfg_mod


def create_yaml_file(path, content: dict):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(content, f)

