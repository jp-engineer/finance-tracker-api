from fastapi import APIRouter
from finance_tracker_shared.schemas import APIResponse
from app.core.helpers import check_e2e_mode

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/e2e-testing")

@router.get("/", response_model=APIResponse)
def get_e2e_mode_check():
    logger.info("GET /e2e-testing/")

    response = {
        "data": check_e2e_mode()
    }
    
    logger.info(response)
    
    return response
