"""
ERP PO Management System — Product API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date

from backend.database import get_db
from backend.auth import get_current_user
from backend.models import User
from backend.schemas import (
    ProductCreate, ProductUpdate, ProductResponse,
    AIDescriptionRequest, AIDescriptionResponse,
)
from backend import crud
from backend.services.ai_service import generate_description

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("", response_model=List[ProductResponse])
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    expiry_before: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve all active products with optional filters."""
    try:
        return crud.get_products(
            db,
            skip=skip,
            limit=limit,
            search=search,
            category=category,
            brand=brand,
            expiry_before=expiry_before,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve a single product by ID."""
    try:
        product = crud.get_product(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new product."""
    try:
        return crud.create_product(db, product.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing product."""
    try:
        updated = crud.update_product(db, product_id, product.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=404, detail="Product not found")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Soft-delete a product."""
    try:
        success = crud.delete_product(db, product_id)
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ai-description", response_model=AIDescriptionResponse)
async def ai_description(
    req: AIDescriptionRequest,
    current_user: User = Depends(get_current_user),
):
    """Generate an AI-powered marketing description for a product."""
    try:
        description = await generate_description(req.product_name, req.category)
        return AIDescriptionResponse(product_name=req.product_name, description=description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")
