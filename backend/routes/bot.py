from fastapi import APIRouter, Query
from services.instagram_service import check_and_respond_to_dm, simulate_bot_response

router = APIRouter()

@router.get("/run")
def run_bot():
    check_and_respond_to_dm()
    return {"status": "Bot is running and checked messages."}

@router.get("/simulate-dm")
def simulate_dm(message: str = Query(...), username: str = Query("tester")):
    response = simulate_bot_response(message, username)
    return {"response": response}