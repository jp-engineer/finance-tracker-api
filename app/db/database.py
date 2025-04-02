import os
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.db.base_class import Base
from app.config import APP_CFG
from app.utils.load_settings_from_files import load_merged_settings
from app.schemas.setting import SettingCreate
from app.db.models.setting import Setting

import logging
logger = logging.getLogger(__name__)

def get_engine():
    db_url = f"sqlite:///{APP_CFG['DB_PATH']}"
    logger.debug(f"Creating database engine with URL: {db_url}")
    return create_engine(db_url, echo=False, future=True)

def init_db():
    if not os.path.exists(APP_CFG["DB_PATH"]):
        logger.debug(f"Database file does not exist. Creating: {APP_CFG['DB_PATH']}")
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
        seed_settings()

def seed_settings():
    settings_data = load_merged_settings()
    engine = get_engine()

    with Session(engine) as session:
        for category, kv in settings_data.items():
            for key, value in kv.items():
                if value is None:
                    if key == "start_date":
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
