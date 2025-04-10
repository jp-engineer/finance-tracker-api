import os
import sys
import importlib
import json

import yaml


CONFIG_PATH = "app.config"
TEST_DATA_DIR = os.path.join("tests", "data")


def reload_config_module():
    if CONFIG_PATH in sys.modules:
        del sys.modules[CONFIG_PATH]
        
    cfg_mod = importlib.import_module(CONFIG_PATH)

    return cfg_mod


def create_yaml_file(path, content: dict):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(content, f)


def load_test_data_file(file_name: str) -> dict:
    
    file_path = os.path.join(TEST_DATA_DIR, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test data file not found: {file_path}")

    data_dict = {}
    if file_name.endswith(".json"):
        with open(file_path, "r", encoding="utf-8") as f:
            data_dict = json.load(f)
    elif file_name.endswith(".yml") or file_name.endswith(".yaml"):
        with open(file_path, "r", encoding="utf-8") as f:
            data_dict = yaml.safe_load(f)
    else:
        raise ValueError("Unsupported file type. Only .json and .yml/.yaml are supported.")
    
    return data_dict