from fastapi import APIRouter
from app.db.utils.get_db_functions import get_all_settings_from_db, get_setting_from_db

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/settings")

# --- Settings Routes ---
@router.get("/get-all-settings")
def get_all_settings():
    logger.info("GET /get-all-settings")
    settings_dict = get_all_settings_from_db()
    return settings_dict

@router.get("/get-setting-by-category-and-key/{category}/{key}")
def get_setting_by_category_and_key(category: str, key: str):
    logger.info(f"GET /get-setting-by-category-and-key/{category}/{key}")
    setting_dict = get_setting_from_db(category, key)
    if setting_dict is None:
        return {"error": "Setting not found"}
    return setting_dict
