from datetime import date

import pytest

from app.config import APP_CFG
from tests.helpers import create_yaml_file

from app.core.helpers import (
    check_e2e_mode,
    read_yaml_file,
    read_json_file,
    write_yaml_file,
    load_user_settings_dict
)

pytestmark = [
    pytest.mark.unit,
    pytest.mark.core
]

def test_check_e2e_mode_in_prod():
    assert check_e2e_mode() is False


def test_check_e2e_mode_in_e2e(monkeypatch):
    monkeypatch.setitem(APP_CFG, "MODE", "e2e_testing")

    assert check_e2e_mode() is True


def test_read_yaml_file_valid_path(tmp_path):
    yaml_content = """
    key: value
    """
    yaml_file = tmp_path / "test.yaml"
    yaml_file.write_text(yaml_content, encoding="utf-8")

    data = read_yaml_file(str(yaml_file))

    assert data == {"key": "value"}


def test_read_yaml_file_invalid_path(tmp_path):
    invalid_yaml_dir = tmp_path
    non_existent_file = str(invalid_yaml_dir / "non_existent.yaml")
    
    data = read_yaml_file(non_existent_file)

    assert data == {}


def test_read_json_file_valid_path(tmp_path):
    json_content = """
    {
        "key": "value"
    }
    """
    json_file = tmp_path / "test.json"
    json_file.write_text(json_content, encoding="utf-8")

    data = read_json_file(str(json_file))

    assert data == {"key": "value"}


def test_read_json_file_invalid_path(tmp_path):
    invalid_json_dir = tmp_path
    non_existent_file = str(invalid_json_dir / "non_existent.json")
    
    data = read_json_file(non_existent_file)

    assert data == {}


def test_write_yaml_file_valid_path(tmp_path):
    yaml_content = {
        "key": "value"
    }
    yaml_file = tmp_path / "test.yaml"

    write_yaml_file(str(yaml_file), yaml_content)

    data = read_yaml_file(str(yaml_file))

    assert data == yaml_content


def test_write_yaml_file_invalid_path(tmp_path):
    invalid_yaml_dir = tmp_path / "non_existent_dir"
    yaml_file = invalid_yaml_dir / "test.yaml"
    yaml_content = {
        "key": "value"
    }

    with pytest.raises(FileNotFoundError):
        write_yaml_file(str(yaml_file), yaml_content)


# def test_load_user_settings_dict_merges_valid(monkeypatch, tmp_path):
#     default_settings = {
#         "general": {
#             "default_currency": "USD",
#             "default_currency_symbol": "$"
#         },
#         "developer": {
#             "start_date": "2024-01-01"
#         }
#     }

#     user_settings = {
#         "general": {
#             "currency": "EUR"
#         },
#         "developer": {
#             "start_date": None
#         }
#     }

#     default_settings_path = tmp_path / "default_user_settings.yml"
#     user_settings_path = tmp_path / "user_settings.yml"
    
#     create_yaml_file(default_settings_path, default_settings)
#     create_yaml_file(user_settings_path, user_settings)

#     monkeypatch.setitem(APP_CFG, "DEFAULT_SETTINGS_DIR", str(tmp_path))
#     monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(user_settings_path))

#     merged = load_user_settings_dict()

#     assert merged["general"]["currency"] == "EUR"
#     assert merged["general"]["default_currency_symbol"] == "$"
#     assert merged["developer"]["start_date"] == date.today().strftime("%Y-%m-%d")


# def test_load_user_settings_dict_raises_on_invalid_category(monkeypatch, tmp_path):
#     default_settings = {
#         "general": {
#             "currency": "USD"
#         }
#     }

#     user_settings = {
#         "invalid_category": {
#             "currency": "EUR"
#         }
#     }

#     default_settings_path = tmp_path / "default_user_settings.yml"
#     user_settings_path = tmp_path / "user_settings.yml"
    
#     create_yaml_file(default_settings_path, default_settings)
#     create_yaml_file(user_settings_path, user_settings)

#     monkeypatch.setitem(APP_CFG, "DEFAULT_SETTINGS_DIR", str(tmp_path))
#     monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(user_settings_path))

#     with pytest.raises(ValueError, match="Category invalid_category not found in default settings."):
#         load_user_settings_dict()


# def test_load_user_settings_dict_raises_on_invalid_key(monkeypatch, tmp_path):
#     default_settings = {
#         "general": {
#             "currency": "USD"
#         }
#     }

#     user_settings = {
#         "general": {
#             "invalid_key": "value"
#         }
#     }

#     default_settings_path = tmp_path / "default_user_settings.yml"
#     user_settings_path = tmp_path / "user_settings.yml"
    
#     create_yaml_file(default_settings_path, default_settings)
#     create_yaml_file(user_settings_path, user_settings)

#     monkeypatch.setitem(APP_CFG, "DEFAULT_SETTINGS_DIR", str(tmp_path))
#     monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(user_settings_path))

#     with pytest.raises(ValueError, match="Key invalid_key in general not found in default settings."):
#         load_user_settings_dict()


# def test_load_user_settings_dict_removes_none_values(monkeypatch, tmp_path):
#     default_settings = {
#         "general": {
#             "currency": "USD",
#             "timezone": "UTC"
#         },
#         "developer": {
#             "start_date": "2024-01-01"
#         }
#     }

#     user_settings = {
#         "general": {
#             "currency": None,
#             "timezone": "Europe/Paris"
#         },
#         "developer": {
#             "start_date": None
#         }
#     }

#     default_settings_path = tmp_path / "default_user_settings.yml"
#     user_settings_path = tmp_path / "user_settings.yml"
    
#     create_yaml_file(default_settings_path, default_settings)
#     create_yaml_file(user_settings_path, user_settings)

#     monkeypatch.setitem(APP_CFG, "DEFAULT_SETTINGS_DIR", str(tmp_path))
#     monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(user_settings_path))

#     result = load_user_settings_dict()

#     assert "currency" in result["general"]  # should fall back to default "USD"
#     assert result["general"]["timezone"] == "Europe/Paris"
#     assert result["developer"]["start_date"] == date.today().strftime("%Y-%m-%d")