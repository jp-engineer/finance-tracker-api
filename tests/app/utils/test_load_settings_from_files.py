import os
import json
import yaml
import pytest
from pathlib import Path
from app.utils.load_settings_from_files import load_merged_settings

def load_test_json(filename: str) -> dict:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = Path(current_dir) / "data" / filename

    with open(path, "r") as f:
        return json.load(f)

@pytest.fixture
def temp_settings_files(tmp_path, monkeypatch):
    user_settings = load_test_json("test_user_settings.json")
    default_settings = load_test_json("test_default_settings.json")

    user_path = tmp_path / "user-settings.yml"
    default_path = tmp_path / "default-settings.yml"
    user_path.write_text(yaml.dump(user_settings))
    default_path.write_text(yaml.dump(default_settings))

    monkeypatch.setattr("app.utils.load_settings_from_files.DEFAULTS_PATH", user_path)
    monkeypatch.setattr("app.utils.load_settings_from_files.FALLBACKS_PATH", default_path)

    return user_settings, default_settings

def test_load_merged_settings(temp_settings_files):
    user, default = temp_settings_files
    merged = load_merged_settings()

    assert merged["general"]["country_code"] == "gb"
    assert merged["view"]["user_name"] == "Alice"
    assert merged["view"]["date_format"] == "yyyy-mm-dd"
    assert merged["developer"]["start_date"] == "2024-01-01"
