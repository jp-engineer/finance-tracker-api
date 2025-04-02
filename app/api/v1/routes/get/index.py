from fastapi import APIRouter
from app.config import APP_CFG

router = APIRouter()

# --- Status messages ---
@router.get("/get-init-message")
def get_index_init_message():
    return {"message": "finance-tracker API is running"}

@router.get("/get-app-config")
def get_index_app_config():
    print(APP_CFG)
    return APP_CFG
