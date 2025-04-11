import pytest
from sqlalchemy.orm import Session

from app.db.models import SettingGeneral, SettingDeveloper, SettingView
from app.core.helpers import read_yaml_file
from app.db.database import get_engine
from app.config import APP_CFG
from tests.helpers import create_yaml_file

from app.core.update_settings import (
    update_settings_in_db_from_dict,
    update_settings_in_file_from_dict,
    update_all_settings_from_dict,
    update_setting_by_category_and_key
)


pytestmark = [
    pytest.mark.unit,
    pytest.mark.core
]


def test_update_settings_in_db_from_dict(empty_db):
    test_engine = get_engine()
    with Session(test_engine) as session:
        session.add_all([
            SettingGeneral(key="default_currency", norm_key="Default currency", value="USD")
        ])
        session.commit()
    
    settings_dict = {
        "general": {
            "default_currency": "EUR"
        }
    }

    update_settings_in_db_from_dict(settings_dict)

    with Session(test_engine) as session:
        updated_setting = session.query(SettingGeneral).filter_by(key="default_currency").first()

    assert updated_setting is not None
    assert updated_setting.value == "EUR"


def test_update_settings_in_db_from_dict_raises_invalid_category(empty_db):
    settings_dict = {
        "invalid_category": {
            "default_currency": "EUR"
        }
    }

    with pytest.raises(ValueError):
        update_settings_in_db_from_dict(settings_dict)


def test_update_settings_in_db_from_dict_raises_invalid_key(empty_db):
    test_engine = get_engine()
    with Session(test_engine) as session:
        session.add_all([
            SettingGeneral(key="default_currency", norm_key="Default currency", value="USD")
        ])
        session.commit()

    settings_dict = {
        "general": {
            "invalid_key": "EUR"
        }
    }

    with pytest.raises(ValueError):
        update_settings_in_db_from_dict(settings_dict)


def test_update_settings_in_file_from_dict(monkeypatch, tmp_path, empty_db):
    test_file_path = tmp_path / "test_settings.yml"
    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(test_file_path))

    start_settings_dict = {
        "general": {
            "default_currency": "EUR"
        }
    }
    create_yaml_file(test_file_path, start_settings_dict)

    update_settings_dict = {
        "general": {
            "default_currency": "USD"
        }
    }

    update_settings_in_file_from_dict(update_settings_dict)

    with open(test_file_path, 'r') as file:
        content = file.read()

    assert "default_currency: USD" in content
                                           

def test_update_settings_in_file_from_dict_raises_invalid_category(monkeypatch, tmp_path):
    test_file_path = tmp_path / "test_settings.yml"
    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(test_file_path))

    settings_dict = {
        "invalid_category": {
            "default_currency": "EUR"
        }
    }

    with pytest.raises(ValueError):
        update_settings_in_file_from_dict(settings_dict)


def test_update_all_settings_from_dict(monkeypatch, tmp_path, empty_db):
    test_file_path = tmp_path / "test_settings.yml"
    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(test_file_path))

    engine = get_engine()
    with Session(engine) as session:
        session.add_all([
            SettingGeneral(key="default_currency", norm_key="Default currency", value="USD"),
            SettingDeveloper(key="start_date", norm_key="Start date", value="2023-01-01")
        ])
        session.commit()

    start_settings_dict = {
        "general": {
            "default_currency": "EUR"
        },
        "developer": {
            "start_date": "2023-01-01"
        }
    }
    create_yaml_file(test_file_path, start_settings_dict)
    settings_to_update = {
        "general": [
                {
                    "key": "default_currency",
                    "value": "EUR"
                }
            ],
            "developer": [
                {
                    "key": "start_date",
                    "value": "2024-01-01"
                }
            ]
        }

    update_all_settings_from_dict(settings_to_update)
    updated_settings = read_yaml_file(APP_CFG["SETTINGS_FILE"])
    expected = {
        "general": {
            "default_currency": "EUR"
        },
        "developer": {
            "start_date": "2024-01-01"
        }
    }

    assert updated_settings == expected
    
    engine = get_engine()
    with Session(engine) as session:
        updated_general = session.query(SettingGeneral).filter_by(key="default_currency").first()
        updated_developer = session.query(SettingDeveloper).filter_by(key="start_date").first()
    
    results_dict = {
        "general": {
            "default_currency": updated_general.value
        },
        "developer": {
            "start_date": updated_developer.value
        }
    }
    
    assert results_dict == expected


def test_update_all_settings_from_dict_raises_invalid_category(monkeypatch, tmp_path):
    test_file_path = tmp_path / "test_settings.yml"
    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(test_file_path))

    settings_dict = {
        "invalid_category": {
            "default_currency": "EUR"
        }
    }

    with pytest.raises(ValueError):
        update_all_settings_from_dict(settings_dict)


def test_update_all_settings_from_dict_raises_invalid_key(monkeypatch, tmp_path):
    test_file_path = tmp_path / "test_settings.yml"
    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(test_file_path))

    settings_dict = {
        "general": [
            {
                "key": "invalid_key",
                "value": "HELLO"
            }
        ]
    }

    with pytest.raises(ValueError):
        update_all_settings_from_dict(settings_dict)


def test_update_all_settings_from_dict_raises_invalid_value(monkeypatch, tmp_path):
    test_file_path = tmp_path / "test_settings.yml"
    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(test_file_path))

    settings_dict = {
        "general": [
            {
                "key": "default_currency",
                "value": 12345
            }
        ]
    }

    with pytest.raises(ValueError):
        update_all_settings_from_dict(settings_dict)


def test_update_setting_by_category_and_key(monkeypatch, tmp_path, empty_db):
    test_file_path = tmp_path / "test_settings.yml"
    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(test_file_path))

    engine = get_engine()
    with Session(engine) as session:
        session.add_all([
            SettingGeneral(key="default_currency", norm_key="Default currency", value="USD")
        ])
        session.commit()

    start_settings_dict = {
        "general": {
            "default_currency": "EUR"
        }
    }
    create_yaml_file(test_file_path, start_settings_dict)

    update_setting_by_category_and_key("general", "default_currency", "GBP")

    updated_settings = read_yaml_file(APP_CFG["SETTINGS_FILE"])
    expected = {
        "general": {
            "default_currency": "GBP"
        }
    }

    assert updated_settings == expected

    engine = get_engine()
    with Session(engine) as session:
        updated_setting = session.query(SettingGeneral).filter_by(key="default_currency").first()

    assert updated_setting.value == "GBP"


def test_update_setting_by_category_and_key_raises_invalid_category(monkeypatch, tmp_path):
    test_file_path = tmp_path / "test_settings.yml"
    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(test_file_path))

    settings_dict = {
        "invalid_category": {
            "default_currency": "EUR"
        }
    }

    with pytest.raises(ValueError):
        update_setting_by_category_and_key("invalid_category", "default_currency", "EUR")


def test_update_setting_by_category_and_key_raises_invalid_key(monkeypatch, tmp_path):
    test_file_path = tmp_path / "test_settings.yml"
    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(test_file_path))

    start_settings_dict = {
        "general": {
            "default_currency": "EUR"
        }
    }
    create_yaml_file(test_file_path, start_settings_dict)

    with pytest.raises(ValueError):
        update_setting_by_category_and_key("general", "invalid_key", "HELLO")


def test_update_setting_by_category_and_key_raises_invalid_value(monkeypatch, tmp_path):
    test_file_path = tmp_path / "test_settings.yml"
    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(test_file_path))

    settings_dict = {
        "general": [
            {
                "key": "default_currency",
                "value": 12345
            }
        ]
    }

    create_yaml_file(test_file_path, settings_dict)

    with pytest.raises(ValueError):
        update_setting_by_category_and_key("general", "default_currency", 12345)