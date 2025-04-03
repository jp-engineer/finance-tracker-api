import os
import gc
import pytest
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from app.db.models.base_class import Base
from app.db.models.setting import Setting
from app.db.database import init_db, seed_settings, engine_context

def test_init_db_creates_file_and_table():
    with engine_context() as engine:
        db_path = engine.url.database

        if os.path.exists(db_path):
            os.remove(db_path)

        init_db(engine)
        assert os.path.exists(db_path)
        assert "settings" in inspect(engine).get_table_names()

        gc.collect()
        engine.dispose()
        os.remove(db_path)

def test_seed_settings_inserts_expected_settings():
    with engine_context() as engine:
        db_path = engine.url.database

        if os.path.exists(db_path):
            os.remove(db_path)

        Base.metadata.create_all(bind=engine)
        seed_settings(engine)

        with Session(engine) as session:
            settings = session.query(Setting).all()
            assert len(settings) > 0
            keys = [s.key for s in settings]
            assert "country_code" in keys
            assert "default_currency" in keys

        gc.collect()
        engine.dispose()
        os.remove(db_path)

# def test_settings_validation_blocks_bad_data(monkeypatch):
#     def bad_settings():
#         return {
#             "general": {"country_code": "xyz"},
#             "view": {"date_format": "invalid-format"},
#             "developer": {"start_date": "2024-01-01"}
#         }

#     engine = get_engine()
#     with Session(engine) as session:
#         session.query(Setting).delete()
#         session.commit()

#     monkeypatch.setattr("app.db.database.load_merged_settings", bad_settings)

#     with Session(engine) as session:
#         seed_settings()
#         assert session.query(Setting).filter_by(key="start_date").first() is not None
#         assert session.query(Setting).filter_by(key="country_code").first() is None
