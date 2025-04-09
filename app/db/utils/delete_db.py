import os
from app.config import APP_CFG

import logging
logger = logging.getLogger(__name__)

def check_for_db_reset() -> None:
    delete_db_flag = os.environ.get("DELETE_DB", "false").strip().lower()
    if delete_db_flag == "true":
        logger.info("DELETE_DB environment variable is set to true. Deleting database.")
        delete_db()

def delete_db() -> None:
    if os.path.exists(APP_CFG['DB_PATH']):
        os.remove(APP_CFG['DB_PATH'])
        logger.info(f"Deleted database file: {APP_CFG['DB_PATH']}")
    else:
        logger.warning(f"Database file does not exist, cannot delete: {APP_CFG['DB_PATH']}")
