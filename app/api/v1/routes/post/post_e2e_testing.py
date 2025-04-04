from fastapi import APIRouter
from app.db.database import re_init_db, seed_settings
import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/e2e-testing")

# --- Status Routes ---
@router.post("/db/post-init-db")
def post_init_blank_test_db():
    logger.info("POST /db/post-init-db")

    re_init_db()
    return {"message": "db initialized"}

@router.post("/db/post-seed-settings")
def post_seed_db_settings_data(data: dict):
    logger.info("POST /db/post-seed-settings")
    
    seed_settings(data)
    return {"message": "settings data seeded", "data": data}

@router.post("/db/post-seed-data")
def post_seed_db_all_data(data: dict):
    logger.info("POST /db/post-seed-data")
    
    # seed_data(data)
    return {"message": "all data seeded"}
