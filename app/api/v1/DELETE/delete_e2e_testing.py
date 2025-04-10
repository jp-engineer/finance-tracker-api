from fastapi import APIRouter
from finance_tracker_shared.schemas import APIResponse
from app.db.utils.delete_db import delete_db
from app.core.helpers import check_e2e_mode

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/e2e-testing")

@router.delete("/db/delete-test-db", response_model=APIResponse)
def delete_test_db():
    logger.info("POST /db/delete-test-db")

    if not check_e2e_mode():
        response = {
            "message": "e2e testing mode is not enabled",
        }
    else:
        delete_db()
        response = {
            "message": "db deleted (if it existed)",
        }

    return response
