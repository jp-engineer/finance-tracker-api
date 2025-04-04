import os
import json
import yaml

DB_PATH = "tests/app/db/test-finances.db"
TEST_DATA_ROOT = "tests/data/"

def load_test_data_file(file_name: str) -> dict:
    file_path = os.path.join(TEST_DATA_ROOT, file_name)
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

def check_test_db_path_exists():
    exists = os.path.exists(DB_PATH)
    return exists
