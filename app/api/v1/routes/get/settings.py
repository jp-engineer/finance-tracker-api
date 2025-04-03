from fastapi import APIRouter

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/settings")

# --- Settings Routes ---

@router.get("/get-all-settings")
def get_all_settings():
    logger.info("GET /get-all-settings")
    return {"message": "This endpoint will return all settings."}
