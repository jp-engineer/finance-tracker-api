import pytest
from sqlalchemy.orm import Session

from app.db.models import SettingGeneral, SettingDeveloper, SettingView

from app.db.database import get_engine
from app.config import APP_CFG

from app.db.crud.read_from_db import (
    get_all_settings_from_db_by_category,
    get_setting_from_db_by_category_and_key
)


def test_get_all_settings_from_db_by_category(empty_db):
    test_engine = get_engine()
    with Session(test_engine) as session:
        session.add_all([
            SettingGeneral(key="default_currency", norm_key="Default currency", value="USD"),
            SettingDeveloper(key="start_date", norm_key="Start date", value="2024-01-01"),
            SettingView(key="date_format", norm_key="Date format", value="YYYY-MM-DD")
        ])
        session.commit()

    result = get_all_settings_from_db_by_category()

    assert "general" in result and "developer" in result and "view" in result
    assert any(setting["key"] == "default_currency" for setting in result["general"].values())
    assert any(setting["key"] == "start_date" for setting in result["developer"].values())
    assert any(setting["key"] == "date_format" for setting in result["view"].values())


def test_get_setting_from_db_by_category_and_key(monkeypatch, seeded_db):
    result = get_setting_from_db_by_category_and_key("general", "default_currency")

    assert result["key"] == "default_currency"
    assert result["norm_key"] == "Default currency"
    assert result["value"] == "EUR"


def test_get_setting_from_db_by_category_and_key_invalid_category(seeded_db):
    with pytest.raises(ValueError):
        get_setting_from_db_by_category_and_key("invalid", "any_key")


def test_get_setting_from_db_by_category_and_key_not_found(seeded_db):
    with pytest.raises(ValueError):
        get_setting_from_db_by_category_and_key("general", "nonexistent_key")