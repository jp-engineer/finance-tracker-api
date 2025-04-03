import yaml
from pathlib import Path
from app.utils.setup_templated_files import setup_templates

import logging
logger = logging.getLogger(__name__)

def load_merged_settings(user_settings_path="app/user/user-settings.yml",
                         default_settings_path="app/defaults/default-settings.yml",
                         templates_dir="app/templates"):

    def read_yaml(path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

    setup_templates(user_settings_path, templates_dir)

    user = read_yaml(user_settings_path)
    default = read_yaml(default_settings_path)
    merged = {}

    for category, keys in default.items():
        merged[category] = {}
        for key, default_val in keys.items():
            user_val = user.get(category, {}).get(key, None)
            merged[category][key] = user_val if user_val is not None else default_val

    logging.debug(f"Merged settings: {merged}")
    return merged