from fastapi import FastAPI, APIRouter
from app.api.v1.routes.get import index as v1_get_index
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='ft-api.log', encoding='utf-8', level=logging.DEBUG)

API_VERSION = "v1"

app = FastAPI(
    title="Finance Tracker API",
    version=API_VERSION
)

api_v1 = APIRouter(prefix=f"/api/{API_VERSION}")
api_v1.include_router(v1_get_index.router)
logger.info(f"API {API_VERSION} initialized with prefix /api/{API_VERSION}")
for route in api_v1.routes:
    logger.info(f"Route added: {route.path} - {route.name} - {route.methods}")

app.include_router(api_v1)
