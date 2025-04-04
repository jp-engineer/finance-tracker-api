from fastapi import APIRouter

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/e2e-testing")

# --- E2E Testing Routes ---
@router.get("/get-e2e-mode-check")
def get_e2e_mode_check():
    logger.info("GET /get-e2e-mode-check")
    return {"status": "e2e-testing is running"}
