# backend/routes/dashboard_data.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def dashboard_info():
    return {"message": "Dashboard endpoint aktif"}
