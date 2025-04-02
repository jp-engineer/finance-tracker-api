import yaml
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

SETTINGS_DIR = Path("app/user")
DEFAULTS_PATH = SETTINGS_DIR / "user-settings.yml"
FALLBACKS_PATH = Path("app/defaults/default-settings.yml")

def load_merged_settings():
    def read_yaml(path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

    user = read_yaml(DEFAULTS_PATH)
    default = read_yaml(FALLBACKS_PATH)
    merged = {}

    for category, keys in default.items():
        merged[category] = {}
        for key, default_val in keys.items():
            user_val = user.get(category, {}).get(key, None)
            merged[category][key] = user_val if user_val is not None else default_val
            
    logging.debug(f"Merged settings: {merged}")

    return merged
    