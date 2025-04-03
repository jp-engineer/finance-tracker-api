import os
import pytest
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from app.db.models.setting import Setting
from app.db.models.base_class import Base
from app.db.database import init_db, seed_settings, engine_context
from app.config import APP_CFG

@pytest.mark.unit
@pytest.mark.db
def test_engine_context_creates_and_disposes_engine():
    with engine_context() as engine:
        assert engine is not None
        assert engine.name == "sqlite"
        assert engine.driver == "pysqlite"

    with pytest.raises(Exception):
        engine.execute("SELECT 1")

@pytest.mark.unit
@pytest.mark.db
def test_init_db_creates_file_and_table():
    with engine_context() as engine:
        db_path = APP_CFG['DB_PATH']
        if os.path.exists(db_path):
            raise Exception(f"Database file already exists: {db_path}")
        
        init_db(engine)
        assert os.path.exists(db_path)
        assert "settings" in inspect(engine).get_table_names()

        engine.dispose()
        os.remove(db_path)

@pytest.mark.unit
@pytest.mark.db
def test_seed_settings_inserts_expected_settings():
    with engine_context() as engine:
        db_path = APP_CFG['DB_PATH']
        if os.path.exists(db_path):
            raise Exception(f"Database file already exists: {db_path}")

        init_db(engine)
        seed_settings(engine)

        with Session(engine) as session:
            settings = session.query(Setting).all()
            assert len(settings) > 0
            keys = [s.key for s in settings]
            assert "country_code" in keys
            assert "default_currency" in keys

        engine.dispose()
        os.remove(db_path)
