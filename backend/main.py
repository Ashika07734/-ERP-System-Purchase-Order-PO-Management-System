"""
ERP PO Management System — FastAPI Application Entry Point
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

from backend.database import engine, Base, get_db
from backend.auth import oauth, create_access_token, get_or_create_user
from backend.routes import vendor_routes, product_routes, po_routes


# ── Lifespan ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup (useful in dev; in prod use migrations)."""
    Base.metadata.create_all(bind=engine)
    yield


# ── App ──────────────────────────────────────────────────
app = FastAPI(
    title="ERP Purchase Order Management System",
    description="Enterprise-grade PO management with immersive UI",
    version="1.0.0",
    lifespan=lifespan,
)

# Session middleware (required by authlib OAuth)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("JWT_SECRET_KEY", "change-me"),
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Mount routers ────────────────────────────────────────
app.include_router(vendor_routes.router)
app.include_router(product_routes.router)
app.include_router(po_routes.router)

# ── Serve frontend static files ──────────────────────────
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


# ══════════════════════════════════════════════════════════
# AUTH ROUTES (not behind JWT)
# ══════════════════════════════════════════════════════════

@app.get("/auth/login")
async def login(request: Request):
    """Initiate Google OAuth flow."""
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", request.url_for("auth_callback"))
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    """Handle Google OAuth callback."""
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to get user info from Google")

        # Get or create user in DB
        user = get_or_create_user(
            db,
            email=user_info["email"],
            full_name=user_info.get("name"),
            picture=user_info.get("picture"),
        )

        # Generate JWT
        access_token = create_access_token(data={"sub": user.email, "uid": user.user_id})

        # Redirect to dashboard with token
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8000")
        return RedirectResponse(
            url=f"{frontend_url}/static/dashboard.html?token={access_token}"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")


@app.post("/auth/dev-login")
async def dev_login(db: Session = Depends(get_db)):
    """
    Development-only login — creates/fetches a test user and returns a JWT.
    Remove this endpoint in production.
    """
    user = get_or_create_user(db, email="admin@erpcloud.io", full_name="Admin User")
    access_token = create_access_token(data={"sub": user.email, "uid": user.user_id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "email": user.email,
            "full_name": user.full_name,
            "picture": user.picture,
            "provider": user.provider,
        },
    }


# ── Health check ─────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "healthy", "service": "ERP PO Management System"}


# ── Root redirect ────────────────────────────────────────
@app.get("/")
def root():
    return RedirectResponse(url="/static/login.html")
