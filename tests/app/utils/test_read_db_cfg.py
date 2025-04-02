import pytest
from app.db.database import init_db
from app.utils.read_db_cfg import get_db_cfg_dict
from app.config import APP_CFG

@pytest.mark.unit
def test_get_db_cfg_before_db_creation(tmp_path, monkeypatch):
    fake_db_path = tmp_path / "fake.db"
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(fake_db_path))

    cfg = get_db_cfg_dict()
    assert cfg["EXISTS"] is False
    assert cfg["HAS_TABLES"] is False
    assert cfg["DB_PATH"] == str(fake_db_path)
    assert cfg["TABLES"] == []

@pytest.mark.unit
def test_get_db_cfg_after_db_creation(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))

    init_db()

    cfg = get_db_cfg_dict()
    assert cfg["EXISTS"] is True
    assert cfg["HAS_TABLES"] is True
    assert "settings" in cfg["TABLES"]
