import os
from sqlalchemy import inspect
from app.config import APP_CFG
from app.db.database import get_engine

import logging
logger = logging.getLogger(__name__)

def get_db_cfg_dict():
    db_path = APP_CFG["DB_PATH"]
    exists = os.path.exists(db_path)

    engine = get_engine()
    inspector = inspect(engine)
    has_settings_table = "settings" in inspector.get_table_names()

    cfg = {
        "DB_PATH": db_path,
        "EXISTS": exists,
        "HAS_TABLES": has_settings_table,
        "TABLES": inspector.get_table_names()
        # "TABLES_COUNT": len(inspector.get_table_names()),
        # "HAS_DATA": False,
        # "SEED_FILE": None
    }
    logger.info(f"DB config: {cfg}")
    
    return cfg
