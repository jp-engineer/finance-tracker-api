from fastapi import APIRouter

from finance_tracker_shared.schemas import APIResponse

from app.core.read_db_cfg import get_db_cfg_dict
from app.config import APP_CFG

import logging
logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/", response_model=APIResponse)
def get_index_message():
    response = {
        "message": "finance-tracker API is running"
    }
    logger.debug(response)
    
    return response


@router.get("/app/get-config", response_model=APIResponse)
def get_index_app_config():
    response = {
        "data": APP_CFG
    }
    logger.debug(response)

    return response


@router.get("/db/get-config", response_model=APIResponse)
def get_index_db_config():
    db_cfg = get_db_cfg_dict()
    response = {
        "data": db_cfg
    }
    logger.debug(response)

    return response