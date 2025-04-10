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


@pytest.mark.parametrize("category, key, value", [
    ("general", "default_currency", "eur"),
    ("general", "default_currency", "EUR")
])
def test_validate_setting_valid(category, key, value):
    assert validate_setting(category, key, value) is True


@pytest.mark.parametrize("category, key, value", [
    ("invalid_category", "key", "value"),
    ("general", "invalid_key", "value"),
    ("general", "default_currency", 123),
])
def test_validate_setting_invalid(category, key, value):
    with pytest.raises(ValueError):
        validate_setting(category, key, value)


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


def test_setup_user_settings_file_creates_user_settings_file(monkeypatch, tmp_path):
    user_settings_file = tmp_path / "user_settings.yml"
    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(user_settings_file))

    setup_user_settings_file()

    assert user_settings_file.exists()


def test_setup_user_settings_file_raises_error_if_template_missing(monkeypatch, tmp_path):
    monkeypatch.setitem(APP_CFG, "TEMPLATE_SETTINGS_DIR", str(tmp_path))
    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(tmp_path / "user_settings.yml"))

    with pytest.raises(FileNotFoundError):
        setup_user_settings_file()


def test_setup_user_settings_file_doesnt_override_existing_values(monkeypatch, tmp_path):
    user_settings_file = tmp_path / "user_settings.yml"
    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(user_settings_file))

    original_content = {"general": {"country_code": "US"}}
    with open(user_settings_file, "w") as f:
        yaml.dump(original_content, f)

    setup_user_settings_file()

    with open(user_settings_file, "r") as f:
        result = yaml.safe_load(f)
        
    assert result['general']['country_code'] == "US"
