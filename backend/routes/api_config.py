# backend/routes/api_config.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_config():
    return {"message": "API Config Endpoint aktif"}
