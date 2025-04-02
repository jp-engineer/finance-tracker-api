import os
import pytest
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from app.db.database import init_db, get_engine, seed_settings
from app.db.models.setting import Setting

def test_init_db_creates_file_and_table():
    engine = get_engine()
    db_path = engine.url.database

    
    if os.path.exists(db_path):
        os.remove(db_path)
    
    init_db()
    assert os.path.exists(db_path)

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "settings" in tables

def test_seed_settings_inserts_expected_settings():
    engine = get_engine()
    session = Session(engine)

    settings = session.query(Setting).all()
    assert len(settings) > 0

    keys = [s.key for s in settings]
    assert "country_code" in keys
    assert "default_currency" in keys
    session.close()

def test_settings_validation_blocks_bad_data(monkeypatch):
    def bad_settings():
        return {
            "general": {"country_code": "xyz"},
            "view": {"date_format": "invalid-format"},
            "developer": {"start_date": "2024-01-01"}
        }

    engine = get_engine()
    with Session(engine) as session:
        session.query(Setting).delete()
        session.commit()

    monkeypatch.setattr("app.db.database.load_merged_settings", bad_settings)

    with Session(engine) as session:
        seed_settings()
        assert session.query(Setting).filter_by(key="start_date").first() is not None
        assert session.query(Setting).filter_by(key="country_code").first() is None
