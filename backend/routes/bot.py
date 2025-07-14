from fastapi import APIRouter
from services.instagram_service import check_and_respond_to_dm

router = APIRouter()

@router.get("/run")
def run_bot():
    check_and_respond_to_dm()
    return {"status": "Bot is running and checked messages."}
