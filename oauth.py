# backend/app/routes/oauth.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/google")
def google_oauth_placeholder():
    return {"message": "Google OAuth will be added later."}
