from fastapi import APIRouter
from finance_tracker_shared.schemas import APIResponse
from app.config import APP_CFG
from app.core.read_db_cfg import get_db_cfg_dict

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=APIResponse)
def get_index_message():
    logger.info("GET /")
    response = {
        "message": "finance-tracker API is running"
    }
    logger.info(response)
    
    return response

@router.get("/app/get-config", response_model=APIResponse)
def get_index_app_config():
    logger.info("GET /app/get-config")
    response = {
        "data": APP_CFG
    }
    logger.info(response)

    return response

@router.get("/db/get-config", response_model=APIResponse)
def get_index_db_config():
    logger.info("GET /db/get-config")
    db_cfg = get_db_cfg_dict()
    response = {
        "data": db_cfg
    }
    logger.info(response)

    return response
