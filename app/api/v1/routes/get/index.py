from fastapi import APIRouter

router = APIRouter()

# --- Status messages ---
@router.get("/get-init-message")
def get_index_init_message():
    return {"message": "finance-tracker API is running"}
