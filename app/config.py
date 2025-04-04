import os
import sys

import logging
logger = logging.getLogger(__name__)

API_VERSION = "v1"
MODE = os.environ.get("MODE", "prod").strip().lower()
MODE_TO_FILENAME = {
    "prod": "finances.db",
    "dev": "dev-finances.db",
    "test": "test-finances.db"
}
if MODE in MODE_TO_FILENAME:
    DB_FILENAME = MODE_TO_FILENAME[MODE]
else:
    logger.error(f"Invalid MODE selected for DB: {MODE}. Exiting.")
    sys.exit(1)
    
if MODE == "test":
    DB_PATH = os.path.join("tests", "app", "db", DB_FILENAME)
    SEED_DIR = os.path.join("tests", "app", "db", "seed")
else:
    DB_PATH = os.path.join("app", "db", DB_FILENAME)
    SEED_DIR = os.path.join("app", "db", "seed")

APP_CFG = {
    "API_VERSION": API_VERSION,
    "MODE": MODE,
    "DB_PATH": DB_PATH,
    "SEED_DIR": SEED_DIR,
}
logger.info(f"App config initialized: {APP_CFG}")
