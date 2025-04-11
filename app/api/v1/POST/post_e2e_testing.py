from fastapi import APIRouter
from finance_tracker_shared.schemas import APIResponse

from app.core.helpers import check_e2e_mode
from app.db.utils.setup_db import re_init_db, seed_setting_tables, init_db, seed_db_with_data

import logging
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/e2e-testing")


@router.post("/db/post-init-db", response_model=APIResponse)
def post_init_blank_test_db():
    if not check_e2e_mode():
        response = {
            "message": "e2e testing mode is not enabled",
            "data": False
        }
    else:
        re_init_db()
        response = {
            "message": "db initialized",
            "data": True
        }
    logger.debug(response)
   
    return response


@router.post("/db/post-seed-settings", response_model=APIResponse)
def post_seed_db_settings_data(data: dict):
    if not check_e2e_mode():
        response = {
            "message": "e2e testing mode is not enabled",
            "data": False
        }
        return response
    else:
        init_db()
        seed_setting_tables(data)

    response = {
        "message": "settings data seeded",
        "data": True
    }
    logger.debug(response)
    
    return response


@router.post("/db/post-seed-test-data", response_model=APIResponse)
def post_seed_test_data(data: dict):
    if not check_e2e_mode():
        response = {
            "message": "e2e testing mode is not enabled",
            "data": False
        }
        return response
    else:
        init_db()
        seed_db_with_data(data)

    response = {
        "message": "test data seeded",
        "data": True
    }
    logger.debug(response)
    
    return response