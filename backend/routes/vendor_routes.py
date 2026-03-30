"""
ERP PO Management System — Vendor API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from backend.database import get_db
from backend.auth import get_current_user
from backend.models import User
from backend.schemas import VendorCreate, VendorUpdate, VendorResponse
from backend import crud

router = APIRouter(prefix="/api/vendors", tags=["Vendors"])


@router.get("", response_model=List[VendorResponse])
def list_vendors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve all active vendors with optional search."""
    try:
        return crud.get_vendors(db, skip=skip, limit=limit, search=search)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{vendor_id}", response_model=VendorResponse)
def get_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve a single vendor by ID."""
    try:
        vendor = crud.get_vendor(db, vendor_id)
        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")
        return vendor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=VendorResponse, status_code=201)
def create_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new vendor."""
    try:
        return crud.create_vendor(db, vendor.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{vendor_id}", response_model=VendorResponse)
def update_vendor(
    vendor_id: int,
    vendor: VendorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing vendor."""
    try:
        updated = crud.update_vendor(db, vendor_id, vendor.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=404, detail="Vendor not found")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{vendor_id}")
def delete_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Soft-delete a vendor."""
    try:
        success = crud.delete_vendor(db, vendor_id)
        if not success:
            raise HTTPException(status_code=404, detail="Vendor not found")
        return {"message": "Vendor deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
