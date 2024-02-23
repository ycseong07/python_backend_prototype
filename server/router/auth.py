from fastapi import APIRouter, Depends, Request, Query, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import quote
import httpx

from server.database.database import SessionLocal
from server.crud.log_crud import create_user
from server.schemas.log_schemas import AuthCreate

router = APIRouter()

from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") 
AUTHORIZATION_URL = os.getenv("AUTHORIZATION_URL") 
TOKEN_URL = os.getenv("TOKEN_URL") 
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID") 
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET") 
REDIRECT_URI = os.getenv("REDIRECT_URI") 

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

scopes = {
    "openid": "OpenID connect to authenticate",
    "profile": "Access to your profile",
    "email": "Access to your email",
}

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTHORIZATION_URL,
    tokenUrl=TOKEN_URL,
    scopes=scopes,
)

@router.get("/login")
async def google_login():
    google_login_url = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    return RedirectResponse(url=google_login_url)

@router.get("/login/callback")
async def google_login_callback(request: Request, code: str = Query(...), db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            TOKEN_URL,
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": REDIRECT_URI
            },
        )
    token_response_json = token_response.json()
    if token_response.is_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=token_response_json,
        )
    
    access_token = token_response_json.get("access_token")
    async with httpx.AsyncClient() as client:
        user_info_response = await client.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    user_info = user_info_response.json()
    
    user_data = AuthCreate(
        user_id=user_info["id"],
        email=user_info["email"],
        full_name=user_info["name"] 
    )
    create_user(db, user=user_data)

    user_email = user_info.get("email")
    user_email_encoded = quote(user_email)

    final_url = f"http://localhost:8501?user_info={user_email_encoded}"
    return RedirectResponse(url=final_url)

@router.get("/logout")
async def logout():
    logout_redirect_url = "http://localhost:8501"
    return RedirectResponse(url=logout_redirect_url)

