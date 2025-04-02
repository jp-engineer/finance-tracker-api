from fastapi import FastAPI, APIRouter
from app.api.v1.routes.get import index as v1_get_index
from app.db.database import init_db
from app.config import APP_CFG

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/ft-api.log', encoding='utf-8', level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

init_db()
logger.info("Database initialized")

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
