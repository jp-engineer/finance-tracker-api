import os
import pytest
from app.config import APP_CFG
from app.db.models.setting import Setting
from app.db.database import (
    init_db,
    get_engine,
    seed_settings,
    load_db_config,
    check_for_db_reset,
)

DEFAULTS_SETTINGS_PATH = "app/defaults/default-settings.yml"
TEST_USER_SETTINGS_PATH = "tests/app/user/test_user-settings.yml"

def test_get_engine_returns_sqlite_engine(monkeypatch):
    monkeypatch.setitem(APP_CFG, "DB_PATH", ":memory:")
    engine = get_engine()
    assert "sqlite" in str(engine.url)

def test_init_db_creates_db_file(tmp_path, monkeypatch):
    test_db_path = tmp_path / "test.db"
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(test_db_path))

    assert not os.path.exists(test_db_path)
    init_db()
    assert os.path.exists(test_db_path)

def test_seed_settings_inserts_valid_data(monkeypatch, tmp_path):
    db_path = tmp_path / "seed.db"
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))

    engine = get_engine()
    init_db(engine)

    settings_dict = {
        "general": {
            "currency": "USD",
            "locale": "en-US"
        },
        "developer": {
            "start_date": None
        }
    }

    seed_settings(settings_dict, engine)
    with engine.connect() as conn:
        result = conn.execute(Setting.__table__.select()).fetchall()
        assert len(result) >= 2

def test_seed_settings_rejects_invalid_data(monkeypatch, tmp_path):
    db_path = tmp_path / "invalid_seed.db"
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))

    engine = get_engine()
    init_db(engine)

    invalid_settings_dict = {
        "general": {
            "currency": 123
        },
        "developer": {
            "start_date": None
        }
    }

    with pytest.raises(Exception):
        seed_settings(invalid_settings_dict, engine)

def test_load_db_config_merges_and_validates_valid_data(monkeypatch):
    monkeypatch.setitem(APP_CFG, "DB_PATH", ":memory:")
    merged = load_db_config(DEFAULTS_SETTINGS_PATH, TEST_USER_SETTINGS_PATH)

    assert isinstance(merged, dict)
    assert "developer" in merged
    assert "general" in merged
    assert "start_date" in merged["developer"]
    assert merged["developer"]["start_date"] is not None

def test_load_db_config_rejects_invalid_keys(monkeypatch):
    monkeypatch.setitem(APP_CFG, "DB_PATH", ":memory:")
    invalid_user_settings_path = {
        "general": {
            "locale": "en-US"
        },
        "developer": {
            "start_date": None
        }
    }
    
    with pytest.raises(Exception):
        load_db_config(DEFAULTS_SETTINGS_PATH, invalid_user_settings_path)


def test_check_for_db_reset_deletes_db(monkeypatch, tmp_path):
    test_db_path = tmp_path / "todelete.db"
    test_db_path.write_text("dummy")
    assert test_db_path.exists()

    monkeypatch.setenv("DELETE_DB", "true")
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(test_db_path))

    check_for_db_reset()
    assert not test_db_path.exists()

def test_check_for_db_reset_does_not_delete_db(monkeypatch, tmp_path):
    test_db_path = tmp_path / "nododelete.db"
    test_db_path.write_text("dummy")
    assert test_db_path.exists()

    monkeypatch.setenv("DELETE_DB", "false")
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(test_db_path))

    check_for_db_reset()
    assert test_db_path.exists()

# import os
# import pytest
# from sqlalchemy.orm import Session
# from sqlalchemy import inspect
# from app.db.models.setting import Setting
# from app.db.models.base_class import Base
# from app.db.database import init_db, seed_settings, engine_context
# from app.config import APP_CFG

# @pytest.mark.unit
# @pytest.mark.db
# def test_engine_context_creates_and_disposes_engine():
#     with engine_context() as engine:
#         assert engine is not None
#         assert engine.name == "sqlite"
#         assert engine.driver == "pysqlite"

#     with pytest.raises(Exception):
#         engine.execute("SELECT 1")

# @pytest.mark.unit
# @pytest.mark.db
# def test_init_db_creates_file_and_table():
#     with engine_context() as engine:
#         db_path = APP_CFG['DB_PATH']

#         init_db(engine)
#         assert os.path.exists(db_path)
#         assert "settings" in inspect(engine).get_table_names()

#         engine.dispose()
#         os.remove(db_path)

# @pytest.mark.unit
# @pytest.mark.db
# def test_seed_settings_inserts_expected_settings():
#     with engine_context() as engine:
#         db_path = APP_CFG['DB_PATH']
#         if os.path.exists(db_path):
#             raise Exception(f"Database file already exists: {db_path}")

#         init_db(engine)
#         seed_settings(engine)

#         with Session(engine) as session:
#             settings = session.query(Setting).all()
#             assert len(settings) > 0
#             keys = [s.key for s in settings]
#             assert "country_code" in keys
#             assert "default_currency" in keys

#         engine.dispose()
#         os.remove(db_path)
