import os
import pytest
import yaml
from app.config import APP_CFG

from app.core.setup_user_settings import (
    validate_setting,
    update_all_user_settings_in_file,
    setup_user_settings_file
)

pytestmark = [
    pytest.mark.unit,
    pytest.mark.core
]

@pytest.fixture
def backup_and_restore_settings_file():
    settings_file = APP_CFG["SETTINGS_FILE"]
    backup_file = settings_file + ".bak"

    if os.path.exists(settings_file):
        os.rename(settings_file, backup_file)

    yield

    if os.path.exists(settings_file):
        os.remove(settings_file)
    if os.path.exists(backup_file):
        os.rename(backup_file, settings_file)

def test_validate_setting_w_lowercase_currency():
    result = validate_setting("general", "default_currency", "eur")
    assert result == True

def test_validate_setting_w_uppercase_currency():
    result = validate_setting("general", "default_currency", "EUR")
    assert result == True

def test_validate_setting_w_invalid_category():
    with pytest.raises(ValueError):
        validate_setting("invalid_category", "key", "value")

def test_validate_setting_w_invalid_key():
    with pytest.raises(ValueError):
        validate_setting("general", "invalid_key", "value")

def test_validate_setting_w_invalid_value():
    with pytest.raises(ValueError):
        validate_setting("general", "default_currency", 123)

def test_update_all_user_settings_in_file_valid(monkeypatch, tmp_path):
    settings_file = tmp_path / "user_settings.yml"
    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(settings_file))

    mock_settings = {"general": {"default_currency": "EUR"}}
    update_all_user_settings_in_file(mock_settings)

    with open(settings_file, encoding="utf-8") as f:
        loaded = yaml.safe_load(f)

    assert loaded["general"]["default_currency"] == "EUR"

def test_update_all_user_settings_in_file_invalid_key_raises():
    mock_settings = {
        "general": {"country_code": "US"},
        "developer": {"start_date": "not-a-date"},
        "invalid": {"key": "bad"}
    }

    with pytest.raises(ValueError):
        update_all_user_settings_in_file(mock_settings)

# update to expect default settings to be loaded
# def test_setup_user_settings_file_creates_user_settings_file(monkeypatch, tmp_path):
#     template_dir = tmp_path / "template_dir"
#     template_dir.mkdir()

#     template_file = template_dir / "user_settings.yml"
#     template_content = {"general": {"default_currency": "EUR"}}
#     with open(template_file, "w") as f:
#         yaml.dump(template_content, f)

#     user_settings_file = tmp_path / "user_settings.yml"

#     monkeypatch.setitem(APP_CFG, "TEMPLATE_SETTINGS_DIR", str(template_dir))
#     monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(user_settings_file))

#     setup_user_settings_file()

#     assert user_settings_file.exists()
#     with open(user_settings_file, "r") as f:
#         loaded = yaml.safe_load(f)
#     assert loaded == template_content

def test_setup_user_settings_file_raises_error_if_template_missing(monkeypatch, tmp_path):
    monkeypatch.setitem(APP_CFG, "TEMPLATE_SETTINGS_DIR", str(tmp_path))
    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(tmp_path / "user_settings.yml"))

    with pytest.raises(FileNotFoundError):
        setup_user_settings_file()

# update to expect default settings to be loaded
# def test_setup_user_settings_file_does_nothing_if_file_exists(monkeypatch, tmp_path):
#     template_dir = tmp_path / "template"
#     template_dir.mkdir()

#     user_settings_file = tmp_path / "user_settings.yml"
#     template_file = template_dir / "user_settings.yml"

#     monkeypatch.setitem(APP_CFG, "TEMPLATE_SETTINGS_DIR", str(template_dir))
#     monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(user_settings_file))

#     original_content = {"preserve": True}
#     with open(user_settings_file, "w") as f:
#         yaml.dump(original_content, f)

#     with open(template_file, "w") as f:
#         yaml.dump({"should_not_overwrite": True}, f)

#     setup_user_settings_file()

#     with open(user_settings_file, "r") as f:
#         result = yaml.safe_load(f)
#     assert result == original_content
