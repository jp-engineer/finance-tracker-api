from fastapi import APIRouter
from app.db.utils.get_db_functions import get_all_settings_from_db

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/settings")

# --- Settings Routes ---

@router.get("/get-all-settings")
def get_all_settings():
    logger.info("GET /get-all-settings")
    settings_dict = get_all_settings_from_db()
    return settings_dict
