import os
import yaml
import pytest
from app.utils.load_settings_from_files import load_merged_settings
from tests.helpers.read_test_data import load_test_json

CWD_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture
def set_temp_settings_files(tmp_path, monkeypatch):
    user_settings = load_test_json(CWD_DIR, "user_settings")
    default_settings = load_test_json(CWD_DIR, "default_settings")

    user_path = tmp_path / "user-settings.yml"
    default_path = tmp_path / "default-settings.yml"
    user_path.write_text(yaml.dump(user_settings))
    default_path.write_text(yaml.dump(default_settings))

    monkeypatch.setattr("app.utils.load_settings_from_files.USER_SETTINGS_PATH", user_path)
    monkeypatch.setattr("app.utils.load_settings_from_files.DEFAULT_SETTINGS_PATH", default_path)

@pytest.mark.unit
def test_load_merged_settings(tmp_path):
    user_settings = load_test_json(CWD_DIR, "user_settings")
    default_settings = load_test_json(CWD_DIR, "default_settings")

    user_path = tmp_path / "user-settings.yml"
    default_path = tmp_path / "default-settings.yml"
    template_dir = tmp_path / "templates"
    template_dir.mkdir()

    user_path.write_text(yaml.dump(user_settings))
    default_path.write_text(yaml.dump(default_settings))

    (template_dir / "user-settings.yml").write_text(yaml.dump(user_settings))

    merged = load_merged_settings(
        user_settings_path=str(user_path),
        default_settings_path=str(default_path),
        templates_dir=str(template_dir)
    )

    assert merged["general"]["country_code"] == user_settings["general"]["country_code"]
    assert merged["view"]["user_name"] == user_settings["view"]["user_name"]
    assert merged["view"]["date_format"] == user_settings["view"]["date_format"]
    assert merged["developer"]["start_date"] == user_settings["developer"]["start_date"]
