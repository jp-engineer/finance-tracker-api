import sys
import importlib

CONFIG_PATH = "app.config"

def reload_config_module():
    if CONFIG_PATH in sys.modules:
        del sys.modules[CONFIG_PATH]
        
    cfg_mod = importlib.import_module(CONFIG_PATH)

    return cfg_mod
