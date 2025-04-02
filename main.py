from fastapi import FastAPI, APIRouter
from app.api.v1.routes.get import index as v1_get_index

API_VERSION = "v1"

app = FastAPI(
    title="Finance Tracker API",
    version=API_VERSION
)

api_v1 = APIRouter(prefix=f"/api/{API_VERSION}")
api_v1.include_router(v1_get_index.router)

app.include_router(api_v1)
