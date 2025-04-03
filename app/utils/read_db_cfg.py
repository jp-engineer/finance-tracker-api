import os
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from app.db.models.setting import Setting
from app.db.database import get_engine
from app.config import APP_CFG

import logging
logger = logging.getLogger(__name__)

def check_entry_in_settings_table(engine):
    with Session(engine) as session:
        count = session.query(Setting).count()
        logger.debug(f"Settings table entry count: {count}")
        return count > 0

def get_db_cfg_dict():
    db_path = APP_CFG["DB_PATH"]
    exists = os.path.exists(db_path)

    engine = get_engine()
    inspector = inspect(engine)

    if not exists:
        logger.warning(f"DB file does not exist at {db_path}.")
        cfg = {
            "DB_PATH": db_path,
            "EXISTS": exists,
            "HAS_TABLES": False,
            "TABLES": [],
            "TABLES_COUNT": 0,
            "HAS_DATA": False
        }
    else:
        cfg = {
            "DB_PATH": db_path,
            "EXISTS": exists,
            "HAS_TABLES": "settings" in inspector.get_table_names(),
            "TABLES": inspector.get_table_names(),
            "TABLES_COUNT": len(inspector.get_table_names()),
            "HAS_DATA": check_entry_in_settings_table(engine)
            # "SEED_FILE": None
        }
        logger.info(f"DB config: {cfg}")
    
    return cfg
