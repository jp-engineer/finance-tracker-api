import os
import yaml
import pytest
from app.utils.file_settings_functions import load_merged_settings, update_all_user_settings
from tests.helpers.read_test_data import load_test_json

CWD_DIR = os.path.dirname(os.path.abspath(__file__))

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
        default_settings_path=str(default_path)
    )

    assert merged["general"]["country_code"] == user_settings["general"]["country_code"]
    assert merged["view"]["user_name"] == user_settings["view"]["user_name"]
    assert merged["view"]["date_format"] == user_settings["view"]["date_format"]
    assert merged["developer"]["start_date"] == user_settings["developer"]["start_date"]

@pytest.mark.unit
def test_invalid_country_code_falls_back_to_default(tmp_path, caplog):
    invalid_user_settings = load_test_json(CWD_DIR, "user_settings_invalid")
    default_settings = load_test_json(CWD_DIR, "default_settings")

    user_path = tmp_path / "user-settings.yml"
    default_path = tmp_path / "default-settings.yml"
    template_dir = tmp_path / "templates"
    template_dir.mkdir()

    user_path.write_text(yaml.dump(invalid_user_settings))
    default_path.write_text(yaml.dump(default_settings))
    (template_dir / "user-settings.yml").write_text(yaml.dump(invalid_user_settings))

    with caplog.at_level("WARNING"):
        merged = load_merged_settings(
            user_settings_path=str(user_path),
            default_settings_path=str(default_path)
        )

    assert merged["general"]["country_code"] == default_settings["general"]["country_code"]
    assert "Invalid setting [general.country_code]" in caplog.text

@pytest.mark.unit
def test_update_all_user_settings_writes_valid_file(tmp_path):
    settings = load_test_json(CWD_DIR, "user_settings")
    user_path = tmp_path / "user-settings.yml"

    result = update_all_user_settings(str(user_path), settings)

    assert user_path.exists()

    with open(user_path, "r", encoding="utf-8") as f:
        written = yaml.safe_load(f)

    assert written["general"] == settings["general"]
    assert written["view"] == settings["view"]
    assert written["developer"] == settings["developer"]

@pytest.mark.unit
def test_update_all_user_settings_invalid_raises(tmp_path):
    invalid_settings = load_test_json(CWD_DIR, "user_settings_invalid")
    user_path = tmp_path / "user-settings.yml"

    with pytest.raises(ValueError) as e:
        update_all_user_settings(str(user_path), invalid_settings)

    assert "Invalid setting" in str(e.value)
