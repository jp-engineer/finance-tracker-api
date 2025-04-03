import os
import yaml
import pytest
from app.utils.load_settings_from_files import load_merged_settings
from tests.helpers.read_test_json import load_test_json


@pytest.fixture
def set_temp_settings_files(tmp_path, monkeypatch):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    user_settings = load_test_json(current_dir, "test_user_settings.json")
    default_settings = load_test_json(current_dir, "test_default_settings.json")

    user_path = tmp_path / "user-settings.yml"
    default_path = tmp_path / "default-settings.yml"
    user_path.write_text(yaml.dump(user_settings))
    default_path.write_text(yaml.dump(default_settings))

    monkeypatch.setattr("app.utils.load_settings_from_files.DEFAULTS_PATH", user_path)
    monkeypatch.setattr("app.utils.load_settings_from_files.FALLBACKS_PATH", default_path)

@pytest.mark.unit
def test_load_merged_settings(set_temp_settings_files):
    merged = load_merged_settings()

    assert merged["general"]["country_code"] == "gb"
    assert merged["view"]["user_name"] == "Alice"
    assert merged["view"]["date_format"] == "yyyy-mm-dd"
    assert merged["developer"]["start_date"] == "2024-01-01"
