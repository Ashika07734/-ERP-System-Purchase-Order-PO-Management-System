"""
ERP PO Management System — Authentication Module
JWT token management and Google OAuth integration.
"""

import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth

from backend.database import get_db
from backend.models import User
from dotenv import load_dotenv

load_dotenv()

# ── JWT Configuration ────────────────────────────────────
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-secret-key")
JWT_ALGORITHM  = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRY_MIN = int(os.getenv("JWT_EXPIRY_MINUTES", "1440"))  # 24 hours

security = HTTPBearer()

# ── Google OAuth Setup ───────────────────────────────────
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID", ""),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET", ""),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generate a signed JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=JWT_EXPIRY_MIN))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """FastAPI dependency — extracts and validates the current user from JWT."""
    payload = decode_token(credentials.credentials)
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject claim",
        )

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )
    return user


def get_or_create_user(db: Session, email: str, full_name: str = None, picture: str = None) -> User:
    """Find an existing user by email or create a new one."""
    user = db.query(User).filter(User.email == email).first()
    if user:
        # Update profile info on each login
        user.full_name = full_name or user.full_name
        user.picture = picture or user.picture
        db.commit()
        db.refresh(user)
        return user

    # Create new user
    user = User(
        email=email,
        full_name=full_name,
        picture=picture,
        provider="google",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
