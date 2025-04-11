import os
import pytest
from sqlalchemy.orm import Session

from app.db.models import SettingGeneral
from app.core.helpers import read_yaml_file, read_json_file
from app.db.database import get_engine
from app.config import APP_CFG

from app.db.utils.setup_db import (
    setup_database,
    init_db,
    seed_db_with_data,
    seed_setting_tables,
    re_init_db
)


pytestmark = [
    pytest.mark.unit,
    pytest.mark.db,
    pytest.mark.utils
    ]


def test_setup_database(monkeypatch, tmp_path):
    user_settings_file = os.path.join("tests", "unit", "app", "user", "test_user_settings.yml")
    db_file = tmp_path / "test.db"

    monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(user_settings_file))
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_file))

    setup_database()

    assert db_file.exists()


def test_setup_database_raises_db_seed_file_not_found(monkeypatch, tmp_path):
    non_existent_seed_file = "non_existent_seed.json"
    db_file = tmp_path / "test.db"

    monkeypatch.setitem(APP_CFG, "DB_SEED_FILE", non_existent_seed_file)
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_file))

    with pytest.raises(FileNotFoundError):
        setup_database()


def test_setup_database_seeds_db(monkeypatch, tmp_path):
    db_file = tmp_path / "test.db"
    test_seed_file = os.path.join("tests", "unit", "app", "db", "seed", "test_sample.json")

    monkeypatch.setitem(APP_CFG, "DB_SEED_FILE", test_seed_file)
    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_file))

    setup_database()

    assert db_file.exists()

    test_engine = get_engine()
    with Session(test_engine) as session:
        result = session.query(SettingGeneral).filter_by(key="default_currency").first()
    
    assert result is not None


def test_init_db(monkeypatch, tmp_path):
    db_file = tmp_path / "test.db"

    monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_file))

    init_db()

    assert db_file.exists()


def test_seed_db_with_data(monkeypatch, empty_db):
    test_seed_file = os.path.join("tests", "unit", "app", "db", "seed", "test_sample.json")
    seed_data = read_json_file(test_seed_file)

    monkeypatch.setitem(APP_CFG, "DB_PATH", str(empty_db))

    seed_db_with_data(seed_data)

    test_engine = get_engine()
    with Session(test_engine) as session:
        result = session.query(SettingGeneral).filter_by(key="default_currency").first()
    
    assert result is not None


def test_seed_db_with_data_raises_developer_start_date_none(monkeypatch, empty_db):
    test_seed_file = os.path.join("tests", "unit", "app", "db", "seed", "test_sample.json")
    seed_data = read_json_file(test_seed_file)
    seed_data["SettingDeveloper"][0]["value"] = None

    monkeypatch.setitem(APP_CFG, "DB_PATH", str(empty_db))

    with pytest.raises(ValueError):
        seed_db_with_data(seed_data)


def test_seed_db_with_data_raises_model_name_not_in_models():
    test_seed_file = os.path.join("tests", "unit", "app", "db", "seed", "test_sample.json")
    seed_data = read_json_file(test_seed_file)
    seed_data["NonExistentModel"] = seed_data.pop("SettingGeneral")

    with pytest.raises(ValueError):
        seed_db_with_data(seed_data)


def test_seed_db_with_data_raises_invalid_value():
    test_seed_file = os.path.join("tests", "unit", "app", "db", "seed", "test_sample.json")
    seed_data = read_json_file(test_seed_file)
    seed_data["SettingGeneral"][0]["value"] = None

    with pytest.raises(ValueError):
        seed_db_with_data(seed_data)


def test_seed_setting_tables(monkeypatch, empty_db):
    user_settings_file = os.path.join("tests", "unit", "app", "user", "test_user_settings.yml")
    settings_dict = read_yaml_file(user_settings_file)

    monkeypatch.setitem(APP_CFG, "DB_PATH", str(empty_db))

    seed_setting_tables(settings_dict)

    test_engine = get_engine()
    with Session(test_engine) as session:
        result = session.query(SettingGeneral).filter_by(key="default_currency").first()
    
    assert result is not None


def test_seed_setting_tables_raises_invalid_category():
    user_settings_file = os.path.join("tests", "unit", "app", "user", "test_user_settings.yml")
    settings_dict = read_yaml_file(user_settings_file)
    settings_dict["invalid_category"] = settings_dict.pop("general")

    with pytest.raises(ValueError):
        seed_setting_tables(settings_dict)


def test_seed_setting_tables_raises_invalid_value():
    user_settings_file = os.path.join("tests", "unit", "app", "user", "test_user_settings.yml")
    settings_dict = read_yaml_file(user_settings_file)
    settings_dict["general"]["default_currency"] = None

    with pytest.raises(ValueError):
        seed_setting_tables(settings_dict)


def test_re_init_db(empty_db):
    test_engine = get_engine()
    with Session(test_engine) as session:
        session.add_all([
            SettingGeneral(key="default_currency", norm_key="Default currency", value="USD")
        ])
        session.commit()
    test_engine.dispose()

    re_init_db()

    with Session(test_engine) as session:
        result = session.query(SettingGeneral).filter_by(key="default_currency").first()
    
    assert result is None