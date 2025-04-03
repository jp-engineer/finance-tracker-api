from fastapi import APIRouter
from app.db.utils.put_db_functions import put_all_settings_to_db

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/settings")

# --- Settings Routes ---
@router.put("/put-all-settings")
def put_all_settings(input_settings: dict):
    logger.info("PUT /put-all-settings")
    put_all_settings_to_db(input_settings)

    return {"message": "Settings updated successfully"}
