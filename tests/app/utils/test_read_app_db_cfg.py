import pytest
pytestmark = [
    pytest.mark.unit, 
    pytest.mark.db,
    pytest.mark.utils,
    pytest.mark.db_utils
]
              
import os
from sqlalchemy.orm import Session
from app.config import APP_CFG
from app.db.database import get_engine, init_db
from app.db.models.setting import Setting
from app.schemas.enums import SettingCategoryEnum
from app.utils.read_app_db_cfg import check_entries_present_in_settings_table, get_db_cfg_dict

@pytest.fixture
def db_with_data(monkeypatch, tmp_path):
    db_path = tmp_path / "test_with_data.db"
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))

    engine = get_engine()
    init_db(engine)

    with Session(engine) as session:
        session.add(Setting(key="currency", value="USD", category=SettingCategoryEnum.view))
        session.commit()

    yield engine

    engine.dispose()
    if db_path.exists():
        os.remove(db_path)

@pytest.fixture
def db_without_data(monkeypatch, tmp_path):
    db_path = tmp_path / "test_without_data.db"
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))

    engine = get_engine()
    init_db(engine)

    yield engine

    engine.dispose()
    if db_path.exists():
        os.remove(db_path)

def test_check_entries_present_in_settings_table_returns_true(db_with_data):
    assert check_entries_present_in_settings_table(db_with_data) is True

def test_check_entries_present_in_settings_table_returns_false(db_without_data):
    assert check_entries_present_in_settings_table(db_without_data) is False

def test_get_db_cfg_dict_with_db_exists(db_with_data):
    cfg = get_db_cfg_dict()

    assert cfg["EXISTS"] is True
    assert cfg["HAS_TABLES"] is True
    assert "settings" in cfg["TABLES"]
    assert cfg["TABLES_COUNT"] >= 1
    assert cfg["HAS_DATA"] is True

def test_get_db_cfg_dict_with_db_does_not_exist(monkeypatch, tmp_path):
    fake_path = tmp_path / "nonexistent.db"
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(fake_path))

    cfg = get_db_cfg_dict()

    assert cfg["EXISTS"] is False
    assert cfg["HAS_TABLES"] is False
    assert cfg["TABLES"] == []
    assert cfg["TABLES_COUNT"] == 0
    assert cfg["HAS_DATA"] is False
