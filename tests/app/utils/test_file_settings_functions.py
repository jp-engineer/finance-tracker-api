import pytest
pytestmark = [
    pytest.mark.unit,
    pytest.mark.utils
]

from datetime import date
import yaml
from app.utils.file_settings_functions import validate_setting, update_all_user_settings

TEST_USER_SETTINGS_PATH = "tests/app/user/test_user-settings.yml"

def test_update_all_user_settings_valid_setting():
    result = validate_setting("general", "currency", "USD")
    assert result is True

def test_update_all_user_settings_invalid_setting_enum_category():
    result = validate_setting("not_a_category", "currency", "USD")
    assert result is False

def test_update_all_user_settings_invalid_setting_value_format():
    result = validate_setting("view", "date_format", "04/04/2025")  # Not ISO-style
    assert result is False

def test_update_all_user_settings_updates_valid_settings_and_writes_file(tmp_path):
    temp_settings_path = tmp_path / "updated-user-settings.yml"

    settings_dict = {
        "general": {
            "currency": "GBP"
        },
        "view": {
            "date_format": "yyyy-mm-dd"
        },
        "developer": {
            "start_date": date.today().strftime("%Y-%m-%d")
        }
    }
    update_all_user_settings(user_settings_path=str(temp_settings_path), settings=settings_dict)

    assert temp_settings_path.exists()

    with open(temp_settings_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data["general"]["currency"] == "GBP"
    assert data["view"]["date_format"] == "yyyy-mm-dd"
    assert data["developer"]["start_date"] == date.today().strftime("%Y-%m-%d")

def test_update_all_user_settings_raises_value_error_on_invalid_setting(tmp_path):
    temp_path = tmp_path / "bad-settings.yml"
    bad_settings = {
        "view": {
            "date_format": "INVALID_FORMAT"
        }
    }

    with pytest.raises(ValueError, match="Invalid setting: view.date_format"):
        update_all_user_settings(user_settings_path=str(temp_path), settings=bad_settings)
