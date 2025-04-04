import pytest
pytestmark = [
    pytest.mark.unit,
    pytest.mark.db,
    pytest.mark.db_utils
]

from sqlalchemy.orm import Session
from app.config import APP_CFG
from app.db.database import get_engine, init_db
from app.db.models.setting import Setting
from app.schemas.enums import SettingCategoryEnum
from app.db.utils.put_db_functions import put_all_settings_to_db

@pytest.fixture(scope="function")
def seeded_db_for_put(monkeypatch, tmp_path):
    db_path = tmp_path / "test_put_settings.db"
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))

    engine = get_engine()
    init_db(engine)

    with Session(engine) as session:
        session.add_all([
            Setting(key="currency", value="USD", category=SettingCategoryEnum.general),
            Setting(key="date_format", value="yyyy-mm-dd", category=SettingCategoryEnum.view),
        ])
        session.commit()

    yield str(db_path)

def test_put_all_settings_to_db_updates_values(seeded_db_for_put):
    updated_settings = {
        "general": {
            "currency": "GBP"
        },
        "view": {
            "date_format": "dd-mm-yyyy"
        }
    }

    put_all_settings_to_db(updated_settings)

    engine = get_engine()
    with Session(engine) as session:
        updated_currency = session.query(Setting).filter_by(key="currency").first()
        updated_format = session.query(Setting).filter_by(key="date_format").first()

        assert updated_currency.value == "GBP"
        assert updated_format.value == "dd-mm-yyyy"

    engine.dispose()

def test_put_all_settings_to_db_raises_on_missing_key(seeded_db_for_put):
    updated_settings = {
        "general": {
            "nonexistent_key": "some value"
        }
    }

    with pytest.raises(ValueError) as exc_info:
        put_all_settings_to_db(updated_settings)

    assert "not found in the database" in str(exc_info.value)
