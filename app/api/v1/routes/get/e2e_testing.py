from fastapi import APIRouter

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/e2e-testing")

# --- E2E Testing Routes ---
@router.get("/")
def get_e2e_mode_check():
    logger.info("GET /e2e-testing/")
    return {"status": "e2e-testing is running"}
