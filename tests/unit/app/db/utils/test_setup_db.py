# import os
# import json
# import yaml
# import pytest
# from datetime import date
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
# from app.config import APP_CFG
# from app.db.models import Base
# # from app.db.models import Setting
# from app.db.database import get_engine

# from app.db.utils.setup_db import (
#     setup_database,
#     init_db,
#     seed_setting_tables,
#     re_init_db,
#     seed_db_with_data
# )

# pytestmark = [
#     pytest.mark.unit,
#     pytest.mark.db,
#     pytest.mark.utils
# ]

# @pytest.fixture
# def temp_user_settings_path(tmp_path):
#     return str(tmp_path / "test_user_settings.yml")

# def test_setup_database_seeds_db_when_seed_file_provided(tmp_path, monkeypatch):
#     db_path = tmp_path / "seed_test.db"
#     seed_file = tmp_path / "test_seed.json"
    
#     seed_file.write_text(json.dumps({
#         "Setting": [{"key": "country_code", "value": "de", "category": "general"}]
#     }))
    
#     monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))
#     monkeypatch.setitem(APP_CFG, "DB_SEED_FILE", str(seed_file))

#     setup_database()

#     engine = get_engine()
#     with Session(engine) as session:
#         result = session.query(Setting).filter_by(key="country_code").first()
#         assert result is not None
#         assert result.value == "de"

# def test_setup_database_seeded_db_has_correct_data(tmp_path, monkeypatch):
#     db_path = tmp_path / "seeded.db"
#     seed_file = tmp_path / "seed.json"
#     seed_file.write_text(json.dumps({
#         "Setting": [{"key": "country_code", "value": "de", "category": "general"}]
#     }))

#     monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))
#     monkeypatch.setitem(APP_CFG, "DB_SEED_FILE", str(seed_file))

#     setup_database()

#     engine = get_engine()
#     with Session(engine) as session:
#         result = session.query(Setting).filter_by(key="country_code").first()
#         assert result is not None
#         assert result.value == "de"


# def test_setup_database_doesnt_seed_db_when_no_seed_file_provided(tmp_path, monkeypatch):
#     db_path = tmp_path / "no_seed.db"
#     monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))
#     monkeypatch.setitem(APP_CFG, "DB_SEED_FILE", None)

#     setup_database()

#     engine = get_engine()
#     with Session(engine) as session:
#         rows = session.query(Setting).all()
#         assert len(rows) > 0  # fallback settings should be inserted


# def test_setup_database_non_seeded_db_has_correct_data(tmp_path, monkeypatch):
#     db_path = tmp_path / "fallback.db"
#     monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))
#     monkeypatch.setitem(APP_CFG, "DB_SEED_FILE", None)

#     setup_database()

#     engine = get_engine()
#     with Session(engine) as session:
#         setting = session.query(Setting).filter_by(key="default_currency").first()
#         assert setting is not None

# def test_init_db_creates_database(db_without_data):
#     # Already initialized by fixture — just confirm DB path was created
#     db_path = APP_CFG["DB_PATH"]
#     assert os.path.exists(db_path)

# def test_seed_db_with_data_inserts_data(db_without_data):
#     seed_db_with_data({
#         "Setting": [{"key": "key", "value": "value", "category": "general"}]
#     }, db_without_data)

#     with Session(db_without_data) as session:
#         rows = session.query(Setting).all()
#         assert len(rows) == 1
#         assert rows[0].key == "key"
#         assert rows[0].value == "value"
#         assert rows[0].category == "general"

# def test_seed_db_with_data_raises_error_on_invalid_model(db_without_data):
#     with pytest.raises(ValueError):
#         seed_db_with_data({"InvalidModel": [{"key": "key", "value": "value", "category": "general"}]}, db_without_data)

# def test_load_settings_dict_validates_user_settings(temp_user_settings_path, monkeypatch):
#     settings_dict = {"developer": {"test_key": "test_value"}}
#     with open(temp_user_settings_path, "w", encoding="utf-8") as f:
#         yaml.dump(settings_dict, f)
#     monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(temp_user_settings_path))

#     with pytest.raises(ValueError):
#         load_settings_dict()

# def test_load_settings_dict_overrides_default_settings(temp_user_settings_path, monkeypatch):
#     settings_dict = {"view": {"default_currency": "USD"}}
#     with open(temp_user_settings_path, "w", encoding="utf-8") as f:
#         yaml.dump(settings_dict, f)
#     monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(temp_user_settings_path))

#     returned_dict = load_settings_dict()

#     assert returned_dict["view"]["default_currency"] == "USD"

# def test_load_settings_dict_sets_empty_start_date_to_today(temp_user_settings_path, monkeypatch):
#     settings_dict = {
#         "developer": {"start_date": None},
#         "view": {"default_currency": "USD"}
#     }
#     with open(temp_user_settings_path, "w", encoding="utf-8") as f:
#         yaml.dump(settings_dict, f)
#     monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(temp_user_settings_path))

#     result = load_settings_dict()

#     assert result["developer"]["start_date"] == date.today().strftime("%Y-%m-%d")

# def test_load_settings_dict_sets_empty_values_to_default(temp_user_settings_path, monkeypatch):
#     settings_dict = {
#         "developer": {"start_date": None},
#         "general": {"currency": None}
#     }
#     with open(temp_user_settings_path, "w", encoding="utf-8") as f:
#         yaml.dump(settings_dict, f)
#     monkeypatch.setitem(APP_CFG, "SETTINGS_FILE", str(temp_user_settings_path))

#     result = load_settings_dict()

#     assert result["developer"]["start_date"] == date.today().strftime("%Y-%m-%d")
#     assert result["view"]["default_currency"] == "gbp"

# def test_seed_settings_table_inserts_data(tmp_path):
#     db_path = tmp_path / "seed_test.db"
#     engine = create_engine(f"sqlite:///{db_path}")
#     Base.metadata.create_all(bind=engine)

#     settings_dict = {
#         "developer": {"start_date": date.today().strftime("%Y-%m-%d")},
#         "general": {"currency": "EUR"}
#     }

#     seed_settings_table(settings_dict, engine)

#     with Session(engine) as session:
#         rows = session.query(Setting).all()
#         assert len(rows) == 2
#         keys = [(r.category, r.key) for r in rows]
#         assert ("developer", "start_date") in keys
#         assert ("general", "currency") in keys

# def test_re_init_db_deletes_file(tmp_path, monkeypatch):
#     db_path = tmp_path / "re_init_test.db"
#     monkeypatch.setitem(APP_CFG, "DB_PATH", str(db_path))

#     # Create the database file
#     with open(db_path, 'w') as f:
#         f.write('test')

#     assert os.path.exists(db_path)

#     re_init_db()

#     assert os.path.exists(db_path)
