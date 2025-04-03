import os
import json
import yaml
from pathlib import Path

def load_test_json(starting_dir: str, filename: str) -> dict:
    starting_dir = os.path.abspath(starting_dir)
    json_path = Path(starting_dir) / "data" / f"test_{filename}.json"

    if not json_path.is_file():
        raise FileNotFoundError(f"File {json_path} does not exist.")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data

def load_test_yaml(starting_dir: str, filename: str) -> dict:
    starting_dir = os.path.abspath(starting_dir)
    yaml_path = Path(starting_dir) / "data" / f"test_{filename}.yml"

    if not yaml_path.is_file():
        raise FileNotFoundError(f"File {yaml_path} does not exist.")

    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
