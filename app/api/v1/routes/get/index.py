from fastapi import APIRouter

router = APIRouter()

# --- Status messages ---
@router.get("/get-status-message")
def get_index_status_message():
    return {"message": "finance-tracker API is running"}
