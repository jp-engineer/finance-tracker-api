# setup logging
import os
import logging
from finance_tracker_shared.utils.setup_logging import setup_app_logging

FILE_LOG_LVL = os.environ.get("FILE_LOG_LEVEL", "DEBUG").strip().upper()
STREAM_LOG_LVL = os.environ.get("STREAM_LOG_LEVEL", "INFO").strip().upper()
setup_app_logging(
    file_level=FILE_LOG_LVL,
    stream_level=STREAM_LOG_LVL
)
logger = logging.getLogger(__name__)

from fastapi import FastAPI, APIRouter
from app.config import APP_CFG
from app.api.v1.GET import get_index as v1_get_index

from app.core.setup_user_settings import setup_user_settings_file
#from app.db.utils.delete_db import check_for_db_reset

setup_user_settings_file()
#check_for_db_reset()
    # setup_database()


app = FastAPI(
    title="Finance Tracker API",
    version=APP_CFG["API_VERSION"]
)

api_v1 = APIRouter(prefix=f"/api/{APP_CFG['API_VERSION']}")

    # from app.api.v1.routes.GET import get_settings as v1_get_settings
    # from app.api.v1.routes.PUT import put_settings as v1_put_settings

api_v1.include_router(v1_get_index.router)
    # api_v1.include_router(v1_get_settings.router)
    # api_v1.include_router(v1_put_settings.router)

    # if APP_CFG.get("MODE") == "e2e_testing":
    #     from app.api.v1.routes.GET import get_e2e_testing as v1_get_e2e_testing
    #     from app.api.v1.routes.POST import post_e2e_testing as v1_post_e2e_testing
    #     from app.api.v1.routes.DELETE import delete_e2e_testing as v1_delete_e2e_testing

    #     api_v1.include_router(v1_get_e2e_testing.router)
    #     api_v1.include_router(v1_post_e2e_testing.router)
    #     api_v1.include_router(v1_delete_e2e_testing.router)

logger.info(f"API {APP_CFG['API_VERSION']} initialized.")
for route in api_v1.routes:
    logger.debug(f"Route added: {route.path} - {route.name} - {route.methods}")

app.include_router(api_v1)
