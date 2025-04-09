import os
from datetime import date
from sqlalchemy.orm import Session
from pydantic import ValidationError
from app.config import APP_CFG
from app.db.models import Base
from app.db.models import SettingGeneral, SettingDeveloper, SettingView
from finance_tracker_shared.schemas import SettingGeneralCreate, SettingDeveloperCreate, SettingViewCreate
from app.db.database import get_engine
# from app.db.utils.seed_db import seed_db_with_data
from app.core.setup_user_settings import update_all_user_settings_in_file
from app.core.helpers import read_json_file, load_settings_dict

import logging
logger = logging.getLogger(__name__)

def setup_database() -> None:
    new_db = init_db()
    if new_db:
        if APP_CFG["DB_SEED_FILE"]:
            if not os.path.exists(APP_CFG["DB_SEED_FILE"]):
                raise FileNotFoundError(f"Seed file not found: {APP_CFG['DB_SEED_FILE']}")
            logger.debug(f"Seeding database with file: {APP_CFG['DB_SEED_FILE']}")
            seed_dict = read_json_file(APP_CFG["DB_SEED_FILE"])
            # seed_db_with_data(seed_dict)

        else:
            logger.debug("No seed file provided, seeding settings.")
            settings_dict = load_settings_dict()
            seed_setting_tables(settings_dict)
            update_all_user_settings_in_file(settings_dict)

def init_db(engine: object=None) -> None:
    new_db = False
    if engine is None:
        engine = get_engine()
        dispose_after = True
    else:
        dispose_after = False

    if not os.path.exists(APP_CFG["DB_PATH"]):
        new_db = True
        logger.debug(f"Database file does not exist. Creating: {APP_CFG['DB_PATH']}.")
        Base.metadata.create_all(bind=engine)

    if dispose_after:
        engine.dispose()

    return new_db

def seed_setting_tables(settings_dict: dict, engine: object=None) -> None:
    if engine is None:
        engine = get_engine()
    logger.debug(f"DB at {APP_CFG['DB_PATH']} with settings: {settings_dict}")

    with Session(engine) as session:
        for category, key_value in settings_dict.items():
            if category == "general":
                for key, value in key_value.items():
                    try:
                        validated = SettingGeneralCreate(key=key, value=value)
                        existing = session.query(SettingGeneral).filter_by(key=key).first()
                        if not existing:
                            db_setting = SettingGeneral(**validated.model_dump())
                            session.add(db_setting)
                            logger.debug(f"Inserted: {key} with value: {value} in category: {category}")
                    except ValidationError as e:
                        raise ValueError(f"Error inserting {key} in category {category}: {e}")
            
            elif category == "developer":
                for key, value in key_value.items():
                    try:
                        if value is None and key == "start_date":
                            value = date.today().strftime("%Y-%m-%d")
                            logger.debug(f"Setting start_date to today, ie: {value}")

                        validated = SettingDeveloperCreate(key=key, value=value)
                        existing = session.query(SettingDeveloper).filter_by(key=key).first()
                        if not existing:
                            db_setting = SettingDeveloper(**validated.model_dump())
                            session.add(db_setting)
                            logger.debug(f"Inserted: {key} with value: {value} in category: {category}")
                    except ValidationError as e:
                        raise ValueError(f"Error inserting {key} in category {category}: {e}")
 
            elif category == "view":
                for key, value in key_value.items():
                    try:
                        validated = SettingViewCreate(key=key, value=value)
                        existing = session.query(SettingView).filter_by(key=key).first()
                        if not existing:
                            db_setting = SettingView(**validated.model_dump())
                            session.add(db_setting)
                            logger.debug(f"Inserted: {key} with value: {value} in category: {category}")
                    except ValidationError as e:
                        raise ValueError(f"Error inserting {key} in category {category}: {e}")

        session.commit()
        engine.dispose()

def re_init_db() -> None:
    if os.path.exists(APP_CFG['DB_PATH']):
        os.remove(APP_CFG['DB_PATH'])
        logger.info(f"Deleted database file: {APP_CFG['DB_PATH']}")

    init_db()
