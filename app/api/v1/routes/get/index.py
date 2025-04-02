from fastapi import APIRouter
from app.config import APP_CFG

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

# --- Status messages ---
@router.get("/get-init-message")
def get_index_init_message():
    logger.info("GET /get-init-message")
    return {"message": "finance-tracker API is running"}

@router.get("/get-app-config")
def get_index_app_config():
    logger.info("GET /get-app-config")
    return APP_CFG
