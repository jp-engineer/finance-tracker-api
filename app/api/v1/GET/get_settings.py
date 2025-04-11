from fastapi import APIRouter

from finance_tracker_shared.schemas import APIResponse

from app.db.crud.read_from_db import get_all_settings_from_db_by_category, get_setting_from_db_by_category_and_key

import logging
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/settings")


@router.get("/get-all-settings", response_model=APIResponse)
def get_all_settings():
    settings = get_all_settings_from_db_by_category()
    message = None
    if not settings:
        message = "No settings found in the database."
    else:
        message = "Settings retrieved successfully."
    
    response = {
        "message": message,
        "data": settings
    }
    logger.debug(response)

    return response


@router.get("/{category}/get-setting-by-key/{key}", response_model=APIResponse)
def get_setting_by_key_and_category_from_db(category: str, key: str):
    setting = get_setting_from_db_by_category_and_key(category, key)
    message = None
    if not setting:
        message = f"Setting with key '{key}' not found."
        success = False
    else:
        message = f"Setting with key '{key}' retrieved successfully."
        success = True
    
    response = {
        "success": success,
        "message": message,
        "data": setting
    }
    logger.debug(response)

    return response