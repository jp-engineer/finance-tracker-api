import logging
import app.utils.setup_app_logging
logger = logging.getLogger(__name__)

from fastapi import FastAPI, APIRouter
from app.config import APP_CFG
from app.db.database import setup_db
from app.api.v1.routes.get import index as v1_get_index
# from app.api.v1.routes.get import settings as v1_get_settings
# from app.api.v1.routes.put import settings as v1_put_settings
from app.api.v1.routes.get import e2e_testing as v1_get_e2e_test
# from app.api.v1.routes.post import e2e_testing as v1_post_e2e_test
# from app.api.v1.routes.delete import e2e_testing as v1_delete_e2e_test

setup_db()

app = FastAPI(
    title="Finance Tracker API",
    version=APP_CFG["API_VERSION"]
)

api_v1 = APIRouter(prefix=f"/api/{APP_CFG['API_VERSION']}")
api_v1.include_router(v1_get_index.router)
# api_v1.include_router(v1_get_settings.router)
# api_v1.include_router(v1_put_settings.router)

if APP_CFG["MODE"] == "e2e_testing":
    api_v1.include_router(v1_get_e2e_test.router)
    # api_v1.include_router(v1_post_e2e_test.router)
    # api_v1.include_router(v1_delete_e2e_test.router)

logger.info(f"API {APP_CFG['API_VERSION']} initialized with prefix: /api/{APP_CFG['API_VERSION']}")
for route in api_v1.routes:
    logger.info(f"Route added: {route.path} - {route.name} - {route.methods}")

app.include_router(api_v1)
