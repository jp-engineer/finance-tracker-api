import pytest
from app import config as app_config

from app.db.utils.delete_db import check_for_db_reset, delete_db

pytestmark = [
    pytest.mark.unit,
    pytest.mark.db,
    pytest.mark.utils
    ]

def test_check_for_db_reset_deletes_when_env_true(monkeypatch, tmp_path):
    db_file = tmp_path / "reset_me.db"
    db_file.write_text("data")

    monkeypatch.setitem(app_config.APP_CFG, "DB_PATH", str(db_file))
    monkeypatch.setenv("DELETE_DB", "true")

    assert db_file.exists()
    check_for_db_reset()
    
    assert not db_file.exists()

def test_check_for_db_reset_does_nothing_if_env_false(monkeypatch, tmp_path):
    db_file = tmp_path / "stay.db"
    db_file.write_text("data")

    monkeypatch.setitem(app_config.APP_CFG, "DB_PATH", str(db_file))
    monkeypatch.setenv("DELETE_DB", "false")

    check_for_db_reset()

    assert db_file.exists()

def test_delete_db_removes_existing_file(monkeypatch, tmp_path):
    db_file = tmp_path / "delete_me.db"
    db_file.write_text("data")

    monkeypatch.setitem(app_config.APP_CFG, "DB_PATH", str(db_file))

    assert db_file.exists()
    delete_db()
    
    assert not db_file.exists()
