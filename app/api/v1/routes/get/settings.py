from fastapi import APIRouter, HTTPException
from app.db.utils.get_db_functions import get_all_settings_from_db, get_setting_from_db
from app.schemas.setting import SettingRead

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/settings")

# --- Settings Routes ---
@router.get("/get-all-settings")
def get_all_settings():
    logger.info("GET /get-all-settings")
    settings_dicts = get_all_settings_from_db()
    return settings_dicts

@router.get("/get-setting-by-category-and-key/{category}/{key}", response_model=SettingRead)
def get_setting_by_category_and_key(category: str, key: str):
    logger.info(f"GET /get-setting-by-category-and-key/{category}/{key}")
    setting_dict = get_setting_from_db(category, key)
    if not setting_dict:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting_dict
