import pytest
pytestmark = [
    pytest.mark.unit,
    pytest.mark.db
]

import os
from sqlalchemy.orm import Session

from app.config import APP_CFG
from app.db.database import get_engine, init_db
from app.db.models.setting import Setting
from app.schemas.enums import SettingCategoryEnum
from app.db.utils.get_db_functions import get_all_settings_from_db, get_setting_from_db

@pytest.fixture
def seeded_db(monkeypatch, tmp_path):
    db_path = tmp_path / "test_settings.db"
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))

    engine = get_engine()
    init_db(engine)

    with Session(engine) as session:
        session.add_all([
            Setting(key="currency", value="USD", category=SettingCategoryEnum.general),
            Setting(key="date_format", value="yyyy-mm-dd", category=SettingCategoryEnum.view),
            Setting(key="start_data", value="2025-04-04", category=SettingCategoryEnum.developer),
        ])
        session.commit()

    yield str(db_path)

    engine.dispose()
    if os.path.exists(db_path):
        os.remove(db_path)

class TestGetSettings:
    def test_get_all_settings_from_db(self, seeded_db):
        settings = get_all_settings_from_db()

        assert isinstance(settings, dict)
        assert "general" in settings
        assert "view" in settings
        assert settings["general"]["currency"] == "USD"
        assert settings["view"]["date_format"] == "yyyy-mm-dd"

    def test_get_setting_from_db_valid_key(self, seeded_db):
        setting = get_setting_from_db("general", "currency")

        assert setting["key"] == "currency"
        assert setting["value"] == "USD"
        assert setting["category"] == "general"

    def test_get_setting_from_db_invalid_category(self, seeded_db):
        result = get_setting_from_db("nonexistent", "currency")
        assert result is None

    def test_get_setting_from_db_invalid_key(self, seeded_db):
        result = get_setting_from_db("general", "nonexistent_key")
        assert result is None
