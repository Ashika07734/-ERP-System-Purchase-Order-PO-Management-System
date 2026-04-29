import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import OAuthCodeRequest, TokenResponse, UserCreate, UserLogin, UserRead
from app.security import create_access_token, hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    user = User(
        email=payload.email,
        name=payload.name,
        role=payload.role,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not user.hashed_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(user.email)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/oauth/google/url")
def oauth_google_url(redirect_uri: str):
    if not settings.oauth_google_client_id:
        raise HTTPException(status_code=400, detail="Google OAuth is not configured")

    base = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": settings.oauth_google_client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    query = "&".join(f"{k}={httpx.QueryParams({k: v})[k]}" for k, v in params.items())
    return {"url": f"{base}?{query}"}


@router.post("/oauth/google", response_model=TokenResponse)
async def oauth_google_exchange(payload: OAuthCodeRequest, db: Session = Depends(get_db)):
    if not settings.oauth_google_client_id or not settings.oauth_google_client_secret:
        raise HTTPException(status_code=400, detail="Google OAuth is not configured")

    token_payload = {
        "code": payload.code,
        "client_id": settings.oauth_google_client_id,
        "client_secret": settings.oauth_google_client_secret,
        "redirect_uri": payload.redirect_uri,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        token_res = await client.post("https://oauth2.googleapis.com/token", data=token_payload)

    if token_res.status_code >= 400:
        raise HTTPException(status_code=400, detail="OAuth token exchange failed")

    access_token = token_res.json().get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="OAuth access token missing")

    async with httpx.AsyncClient(timeout=20.0) as client:
        info_res = await client.get(
            "https://openidconnect.googleapis.com/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    if info_res.status_code >= 400:
        raise HTTPException(status_code=400, detail="Failed to fetch user info")

    info = info_res.json()
    email = info.get("email")
    subject = info.get("sub")
    if not email or not subject:
        raise HTTPException(status_code=400, detail="Incomplete user info from Google")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            name=info.get("name") or email.split("@")[0],
            oauth_provider="google",
            oauth_subject=subject,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token(user.email)
    return TokenResponse(access_token=token)
