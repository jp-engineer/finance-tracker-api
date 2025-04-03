import logging
import app.utils.setup_app_logging
logger = logging.getLogger(__name__)

from fastapi import FastAPI, APIRouter
from app.config import APP_CFG
from app.config import check_for_db_reset
from app.api.v1.routes.get import index as v1_get_index
from app.api.v1.routes.get import settings as v1_get_settings
from app.api.v1.routes.put import settings as v1_put_settings
from app.db.database import init_db, seed_settings
from app.utils.setup_templated_files import setup_templates

TEMPLATES_DIR = "app/templates/"
USER_SETTINGS_PATH = "app/user/user-settings.yml"

def setup_prod_db():
    setup_templates(TEMPLATES_DIR, USER_SETTINGS_PATH)
    logger.info(f"Templates setup completed. User settings path: {USER_SETTINGS_PATH}")

    init_db()
    logger.info("Database initialized.")

    seed_settings()
    logger.info(f"Database seeded at {APP_CFG['DB_PATH']} with settings.")

check_for_db_reset()
if APP_CFG['MODE'] == "prod":
    setup_prod_db()
    
app = FastAPI(
    title="Finance Tracker API",
    version=APP_CFG["API_VERSION"]
)

api_v1 = APIRouter(prefix=f"/api/{APP_CFG['API_VERSION']}")
api_v1.include_router(v1_get_index.router)
api_v1.include_router(v1_get_settings.router)
api_v1.include_router(v1_put_settings.router)

logger.info(f"API {APP_CFG['API_VERSION']} initialized with prefix: /api/{APP_CFG['API_VERSION']}")
for route in api_v1.routes:
    logger.info(f"Route added: {route.path} - {route.name} - {route.methods}")

app.include_router(api_v1)
