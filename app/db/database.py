import os
from datetime import date
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.config import APP_CFG
from app.db.models.base_class import Base
from app.db.models.setting import Setting
from app.schemas.setting import SettingCreate
from app.utils.file_settings_functions import load_merged_settings

import logging
logger = logging.getLogger(__name__)

@contextmanager
def engine_context():
    engine = get_engine()
    try:
        yield engine
    finally:
        engine.dispose()

def get_engine():
    db_url = f"sqlite:///{APP_CFG['DB_PATH']}"
    logger.debug(f"Creating database engine for URL: {db_url}")
    engine = create_engine(db_url, echo=False, future=True)

    return engine

def init_db(engine=None):
    if engine is None:
        engine = get_engine()
        dispose_after = True
    else:
        dispose_after = False

    if not os.path.exists(APP_CFG["DB_PATH"]):
        logger.debug(f"Database file does not exist. Creating: {APP_CFG['DB_PATH']}.")
        Base.metadata.create_all(bind=engine)

    if dispose_after:
        engine.dispose()

def seed_settings(engine=None):
    if engine is None:
        engine = get_engine()

    with Session(engine) as session:
        settings_data = load_merged_settings()
        for category, key_value in settings_data.items():
            for key, value in key_value.items():
                if value is None and key == "start_date":
                    value = date.today().strftime("%Y-%m-%d")
                try:
                    validated = SettingCreate(key=key, value=value, category=category)
                    existing = session.query(Setting).filter_by(key=key, category=category).first()
                    if not existing:
                        db_setting = Setting(**validated.model_dump())
                        session.add(db_setting)
                        logger.info(f"Inserted: {key} in category {category}")
                except Exception as e:
                    logger.error(f"Validation failed for {category}.{key}: {value} | {e}")
        session.commit()
