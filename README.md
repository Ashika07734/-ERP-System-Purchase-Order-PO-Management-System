# GroceryERP Full-Stack Conversion

This workspace now runs locally without Docker.

- Backend: FastAPI (Python)
- Frontend: HTML + CSS + JS
- Database: PostgreSQL
- Auth: JWT + Google OAuth (optional)
- AI: OpenAI or Gemini via environment switch

## Project Structure

- `backend/` FastAPI app and API routes
- `frontend/` static frontend files
- `.env.example` environment template
- `docs/system-architecture.md` architecture and design notes
- `backend/sql/schema.sql` SQL schema (reference)

## Quick Start (No Docker)

1. Create env file:
   - Windows PowerShell: `Copy-Item .env.example .env`
2. Ensure local PostgreSQL is running and create database `groceryerp`.
3. Install dependencies:
   - `cd backend`
   - `pip install -r requirements.txt`
4. Run API:
   - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
5. Run frontend (from workspace root):
   - `python -m http.server 8082`
6. Open:
   - Frontend: `http://localhost:8082/frontend/index.html`
   - Backend docs: `http://localhost:8000/docs`

## API Summary

- Auth:
   - `POST /api/v1/auth/register`
   - `POST /api/v1/auth/login`
   - `GET /api/v1/auth/me`
   - `GET /api/v1/auth/oauth/google/url`
   - `POST /api/v1/auth/oauth/google`
- Products:
   - `GET /api/v1/products`
   - `POST /api/v1/products`
- Vendors:
   - `GET /api/v1/vendors`
   - `POST /api/v1/vendors`
   - `GET /api/v1/vendors/{id}`
   - `PUT /api/v1/vendors/{id}`
   - `DELETE /api/v1/vendors/{id}`
   - `GET /api/v1/vendors/{id}/pos`
- Stock:
   - `GET /api/v1/stock`
   - `GET /api/v1/stock/low-stock`
   - `GET /api/v1/stock/expiring`
   - `POST /api/v1/stock/adjust`
   - `POST /api/v1/stock/batches`
- Purchase Orders:
   - `GET /api/v1/purchase-orders`
   - `POST /api/v1/purchase-orders`
   - `GET /api/v1/purchase-orders/{id}`
   - `PUT /api/v1/purchase-orders/{id}`
   - `POST /api/v1/purchase-orders/{id}/approve`
   - `POST /api/v1/purchase-orders/{id}/send`
   - `POST /api/v1/purchase-orders/{id}/receive`
   - `GET /api/v1/purchase-orders/{id}/pdf`
- Alerts:
   - `GET /api/v1/alerts`
   - `PUT /api/v1/alerts/{id}/resolve`
   - `PUT /api/v1/alerts/read-all`
   - `POST /api/v1/alerts/trigger`
- Reports:
   - `GET /api/v1/reports/stock-valuation`
   - `GET /api/v1/reports/expiry-analysis`
   - `GET /api/v1/reports/vendor-performance`
   - `GET /api/v1/reports/purchase-history`
   - `GET /api/v1/reports/low-stock`
- AI:
   - `POST /api/v1/ai/chat` (JWT required)

## Architecture Assets

- Architecture overview and decision log: `docs/system-architecture.md`
- PostgreSQL schema script: `backend/sql/schema.sql`
- Background scheduler jobs: `backend/app/jobs.py`

## Notes

- JWT token is expected in `Authorization: Bearer <token>`.
- AI provider is controlled by `AI_PROVIDER` in `.env`.
- Google OAuth endpoints are optional and require Google client credentials.
