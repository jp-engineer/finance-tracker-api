from fastapi import APIRouter
from app.utils.read_app_db_cfg import get_db_cfg_dict
from app.config import APP_CFG

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

# --- Status Routes ---
@router.get("/")
def get_index_init_message():
    logger.info("GET /")
    return {"message": "finance-tracker API is running"}

@router.get("/app/get-config")
def get_index_app_config():
    logger.info("GET /app/get-config")
    return APP_CFG

@router.get("/db/get-config")
def get_index_db_config():
    logger.info("GET /db/get-config")
    db_cfg = get_db_cfg_dict()
    return db_cfg
