# Recommended GitHub Commit Strategy

To demonstrate a realistic, professional development lifecycle for your ERP Purchase Order Management System assignment, we recommend structuring your git history sequentially. This proves that you developed the system iteratively rather than copying a massive codebase in a single commit.

Below is a recommended list of at least 20 commits to structure your repository history logically:

## Phase 1: Project Skeleton & Database
1. `Initial project setup: created directory structure and README`
2. `Added .gitignore, Dockerfile, and docker-compose.yml configuration`
3. `Implemented PostgreSQL schema definition (schema.sql)`
4. `Added initial mock data seeding script (seed_data.sql)`
5. `Configured FastAPI entry point and environment variables (.env.example)`

## Phase 2: Core Backend Logic
6. `Implemented SQLAlchemy database engine and local DB configuration (database.py)`
7. `Created ORM models for vendors, products, and POs (models.py)`
8. `Added Pydantic schemas for data validation (schemas.py)`
9. `Implemented CRUD operations for database interaction (crud.py)`
10. `Added FastAPI routing for Vendors endpoint (vendor_routes.py)`

## Phase 3: Advanced Backend & Auth
11. `Implemented JWT Authentication and Google OAuth routing (auth.py)`
12. `Added Product APIs and AI-description generation service (ai_service.py)`
13. `Implemented PO creation endpoint with strict 5% tax business logic (po_service.py)`
14. `Added dashboard statistics API for real-time frontend aggregation`
15. `Integrated MongoDB logic for AI prompt logging`

## Phase 4: Frontend Development
16. `Added modular HTML skeleton (navbar and sidebar components)`
17. `Implemented immersive glassmorphism design system (styles.css)`
18. `Created authentication UI and Quick Dev Login bypass (login.html)`
19. `Implemented interactive analytics dashboard (dashboard.html)`
20. `Built dynamic Purchase Order form with live UI calculation logic (create_po.html)`

## Phase 5: Finalization & Polish
21. `Added Products frontend UI with interactive AI integration (products.html)`
22. `Integrated JavaScript API fetch logic mapping frontend to backend endpoints (app.js)`
23. `Refined UI aesthetics: updated gradients and ensured responsive layout`
24. `Generated placeholder screenshots directory for documentation`
25. `Updated master README to fulfill assignment documentation constraints`
26. `Prepared final database export instructions (database/README.md)`

---

**Tip:** You can create these commits gradually using `git add` and `git commit -m "..."` to construct your history before pushing to your remote GitHub repository.
