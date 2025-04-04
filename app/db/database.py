import os
from datetime import date
from contextlib import contextmanager
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.config import APP_CFG
from app.db.models.base_class import Base
from app.db.models.setting import Setting
from app.schemas.setting import SettingCreate
from app.utils.setup_templated_files import setup_templates
from app.utils.file_settings_functions import update_all_user_settings

import logging
logger = logging.getLogger(__name__)

TEMPLATE_SETTINGS_PATH = "app/templates/user-settings.yml"
DEFAULTS_SETTINGS_PATH = "app/defaults/default-settings.yml"
USER_SETTINGS_PATH = "app/user/user-settings.yml"

TEST_USER_SETTINGS_PATH = "tests/app/user/test_user-settings.yml"

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

def seed_settings(settings_dict, engine=None):
    if engine is None:
        engine = get_engine()
    logger.debug(f"DB at {APP_CFG['DB_PATH']} with settings: {settings_dict}")

    with Session(engine) as session:
        for category, key_value in settings_dict.items():
            for key, value in key_value.items():
                if value is None and key == "start_date":
                    value = date.today().strftime("%Y-%m-%d")
                    logger.debug(f"Setting start_date to today, ie: {value}")
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

def load_db_config(default_settings_path, user_settings_path):
    def read_yaml_file(file_path):
        logger.debug(f"Reading YAML file: {file_path}")
        data = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
        else:
            logger.warning(f"File not found: {file_path}. Using empty configuration.")
        return data

    user_data_dict = read_yaml_file(user_settings_path)
    default_data_dict = read_yaml_file(default_settings_path)

    for category, keys in user_data_dict.items():
        for key, value in list(keys.items()):
            if value is None:
                if key != 'start_date':
                    del user_data_dict[category][key]
                    logger.debug(f"Removed empty value for {category}.{key}")

    merged_data_dict = {**default_data_dict, **user_data_dict}
    logger.debug(f"Merged settings: {merged_data_dict}")

    if merged_data_dict['developer']['start_date'] is None:
        merged_data_dict['developer']['start_date'] = date.today().strftime("%Y-%m-%d")
        logger.debug(f"Set start_date to today: {merged_data_dict['developer']['start_date']}")

    return merged_data_dict

def check_for_db_reset():
    delete_db = os.environ.get("DELETE_DB", "false").strip().lower()
    if delete_db == "true":
        if os.path.exists(APP_CFG['DB_PATH']):
            os.remove(APP_CFG['DB_PATH'])
            logger.info(f"Deleted database file: {APP_CFG['DB_PATH']}")
        else:
            logger.warning(f"Database file does not exist, cannot delete: {APP_CFG['DB_PATH']}")

def setup_db():
    check_for_db_reset()

    if APP_CFG['MODE'] == "prod":
        logger.info("Setting up production database.")
        setup_templates(TEMPLATE_SETTINGS_PATH, USER_SETTINGS_PATH)
        init_db()

        db_settings = load_db_config(DEFAULTS_SETTINGS_PATH, USER_SETTINGS_PATH)
        seed_settings(db_settings)
        update_all_user_settings(USER_SETTINGS_PATH, db_settings)
        
    if APP_CFG['MODE'] == "e2e_test":
        logger.info("Setting up e2e test database.")
        pass

    # # remove and use test fixtures instead
    # if APP_CFG['MODE'] == "test":
    #     logger.info("Setting up test database.")
    #     setup_templates(TEMPLATE_SETTINGS_PATH, TEST_USER_SETTINGS_PATH)
    #     init_db()

    #     db_settings = load_db_config(DEFAULTS_SETTINGS_PATH, TEST_USER_SETTINGS_PATH)
    #     seed_settings(db_settings)
    #     update_all_user_settings(TEST_USER_SETTINGS_PATH, db_settings)
