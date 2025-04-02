from app.config import APP_CFG
from app.db.database import get_engine
from sqlalchemy import inspect
import os

def get_db_cfg_dict():
    db_path = APP_CFG["DB_PATH"]
    exists = os.path.exists(db_path)

    engine = get_engine()
    inspector = inspect(engine)
    has_settings_table = "settings" in inspector.get_table_names()

    cfg = {
        "DB_PATH": db_path,
        "EXISTS": exists,
        "HAS_TABLES": has_settings_table
    }
    
    return cfg
