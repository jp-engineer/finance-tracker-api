import os
from sqlalchemy import inspect
# 5from sqlalchemy.orm import Session
from app.config import APP_CFG
# from app.db.models.setting import Setting
from app.db.database import engine_context

import logging
logger = logging.getLogger(__name__)

# def check_entries_present_in_settings_table(engine: object) -> bool:
#     with Session(engine) as session:
#         count = session.query(Setting).count()
#         logger.debug(f"settings table entry count: {count}")

#         return count > 0

def get_db_cfg_dict() -> dict:
    db_path = APP_CFG["DB_PATH"]
    exists = os.path.exists(db_path)

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
        logger.info(f"DB config: {cfg}")

        return cfg

    with engine_context() as engine:
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        # has_settings_table = "settings" in table_names
        # has_data = check_entries_present_in_settings_table(engine) if has_settings_table else False

        cfg = {
            "DB_PATH": db_path,
            "EXISTS": exists,
            # "HAS_TABLES": has_settings_table,
            "TABLES": table_names,
            "TABLES_COUNT": len(table_names)
            # "HAS_DATA": has_data
        }

        logger.info(f"DB config: {cfg}")

        return cfg
