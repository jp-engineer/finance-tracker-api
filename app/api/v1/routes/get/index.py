import os
from fastapi import APIRouter
from app.config import APP_CFG
from app.utils.read_db_cfg import get_db_cfg_dict

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

# --- Status Routes ---
@router.get("/get-init-message")
def get_index_init_message():
    logger.info("GET /get-init-message")
    return {"message": "finance-tracker API is running"}

@router.get("/get-app-config")
def get_index_app_config():
    logger.info("GET /get-app-config")
    return APP_CFG

@router.get("/get-db-config")
def get_index_db_config():
    logger.info("GET /get-db-config")
    db_cfg = get_db_cfg_dict()
    return db_cfg
