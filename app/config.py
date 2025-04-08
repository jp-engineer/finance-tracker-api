import os
import sys
from typing import Optional

import logging
logger = logging.getLogger(__name__)

def validate_file(filename: str, filetype: str) -> Optional[str]:
    if filetype == "json":
        if not filename.endswith(".json"):
            if "." in filename:
                logger.error(f"Invalid file extension for {filename}. Expected .json")
                return None
            else:
                filename += ".json"
                logger.debug(f"File extension missing, added .json to filename.")

    elif filetype == "yaml":
        if not (filename.endswith(".yaml") or filename.endswith(".yml")):
            if "." in filename:
                logger.error(f"Invalid file extension for {filename}. Expected .yaml or .yml")
                return None
            else:
                filename += ".yml"
                logger.debug(f"File extension missing, added .yml to filename.")

        if not os.path.exists(filename):
            alternate_ext = ".yaml" if filename.endswith(".yml") else ".yml"
            alt_filename = filename.rsplit(".", 1)[0] + alternate_ext
            if os.path.exists(alt_filename):
                logger.debug(f"File {filename} not found. Using alternate file {alt_filename}.")
                filename = alt_filename
            else:
                logger.error(f"File {filename} does not exist.")
                return None

    if not os.path.exists(filename):
        logger.error(f"File {filename} does not exist.")
        return None

    logger.info(f"File {filename} exists.")
    return filename

API_VERSION = "v1"

MODE = os.environ.get("MODE", "prod").strip().lower()
MODE_TO_FILENAME = {
    "prod": "finances.db",
    "dev": "dev-finances.db",
    "e2e_testing": "test-finances.db",
}
if MODE in MODE_TO_FILENAME:
    DB_FILENAME = MODE_TO_FILENAME[MODE]
else:
    logger.error(f"Invalid MODE selected for DB: {MODE}. Exiting.")
    sys.exit(1)

DB_SEED_FILE = os.environ.get("DB_SEED_FILE", None)
SETTINGS_FILE = os.environ.get("SETTINGS_FILE", None)

if MODE == "e2e_testing":
    DB_PATH = os.path.join("tests", "app", "db", DB_FILENAME)
    SEED_DIR = os.path.join("tests", "app", "db", "seed")

    if DB_SEED_FILE is None:
        DB_SEED_FILE = os.path.join(SEED_DIR, "test_seed.json")
    else:
        seed_file_location = os.path.join(SEED_DIR, DB_SEED_FILE)
        seed_file_str = validate_file(seed_file_location, "json")
        if seed_file_str is None:
            logger.error(f"Invalid DB_SEED_FILE: {seed_file_location}. Exiting.")
            sys.exit(1)
        DB_SEED_FILE = seed_file_str

    if SETTINGS_FILE is None:
        SETTINGS_FILE = os.path.join("tests", "app", "user", "test_user_settings.yml")
    else:
        settings_file_location = os.path.join("tests", "app", "user", SETTINGS_FILE)
        settings_file_str = validate_file(settings_file_location, "yaml")
        if settings_file_str is None:
            logger.error(f"Invalid SETTINGS_FILE: {settings_file_location}. Exiting.")
            sys.exit(1)
        SETTINGS_FILE = settings_file_str

else:
    db_path = os.path.join("app", "db", DB_FILENAME)
    DB_PATH = os.environ.get("DB_PATH", db_path)
    SEED_DIR = os.path.join("app", "db", "seed")
    
    if MODE == "dev":
        if DB_SEED_FILE is None:
            if os.path.exists(os.path.join("app", "db", "seed", "dev_seed.json")):
                DB_SEED_FILE = os.path.join("app", "db", "seed", "dev_seed.json")
            else:
                DB_SEED_FILE = None
        else:
            seed_file_location = os.path.join(SEED_DIR, DB_SEED_FILE)
            seed_file_str = validate_file(seed_file_location, "json")
            if seed_file_str is None:
                logger.error(f"Invalid DB_SEED_FILE: {seed_file_location}. Exiting.")
                sys.exit(1)
            DB_SEED_FILE = seed_file_str
        
        if SETTINGS_FILE is None:
            if os.path.exists(os.path.join("app", "user", "dev_user_settings.yml")):
                SETTINGS_FILE = os.path.join("app", "user", "dev_user_settings.yml")
            else:
                SETTINGS_FILE = os.path.join("app", "user", "user_settings.yml")
        else:
            settings_file_location = os.path.join("app", "user", SETTINGS_FILE)
            settings_file_str = validate_file(settings_file_location, "yaml")
            if settings_file_str is None:
                logger.error(f"Invalid SETTINGS_FILE: {settings_file_location}. Exiting.")
                sys.exit(1)
            SETTINGS_FILE = settings_file_str
    
    else:
        if DB_SEED_FILE:
            seed_file_location = os.path.join(SEED_DIR, DB_SEED_FILE)
            seed_file_str = validate_file(seed_file_location, "json")
            if seed_file_str is None:
                logger.error(f"Invalid DB_SEED_FILE: {seed_file_location}. Exiting.")
                sys.exit(1)
            DB_SEED_FILE = seed_file_str
        
        if SETTINGS_FILE is None:
            SETTINGS_FILE = os.path.join("app", "user", "user_settings.yml")
        else:
            settings_file_location = os.path.join("app", "user", SETTINGS_FILE)
            settings_file_str = validate_file(settings_file_location, "yaml")
            if settings_file_str is None:
                logger.error(f"Invalid SETTINGS_FILE: {settings_file_location}. Exiting.")
                sys.exit(1)
            SETTINGS_FILE = settings_file_str

APP_CFG = {
    "API_VERSION": API_VERSION,
    "MODE": MODE,
    "DB_PATH": DB_PATH,
    "DB_SEED_FILE": DB_SEED_FILE,
    "TEMPLATE_SETTINGS_DIR": os.path.join("app", "templates"),
    "DEFAULT_SETTINGS_DIR": os.path.join("app", "defaults"),
    "SETTINGS_FILE": SETTINGS_FILE
}
logger.debug(f"App config: {APP_CFG}")
