from fastapi import FastAPI, APIRouter
from app.api.v1.routes.get import index as v1_get_index
from app.db.database import init_db, seed_settings
from app.config import check_for_db_reset
from app.config import APP_CFG
from app.utils.setup_templated_files import setup_templates

import logging
from app.utils.setup_app_logging import setup_app_logging
setup_app_logging()
logger = logging.getLogger(__name__)

check_for_db_reset()
if APP_CFG['MODE'] == "prod":
    init_db()
    logger.info("Database initialized.")
    seed_settings()
    logger.info("Database seeded with settings.")

app = FastAPI(
    title="Finance Tracker API",
    version=APP_CFG["API_VERSION"]
)

api_v1 = APIRouter(prefix=f"/api/{APP_CFG['API_VERSION']}")
api_v1.include_router(v1_get_index.router)

logger.info(f"API {APP_CFG['API_VERSION']} initialized with prefix: /api/{APP_CFG['API_VERSION']}")
for route in api_v1.routes:
    logger.info(f"Route added: {route.path} - {route.name} - {route.methods}")

app.include_router(api_v1)
