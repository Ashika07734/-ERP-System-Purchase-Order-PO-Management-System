"""
ERP PO Management System — Purchase Order API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from backend.database import get_db
from backend.auth import get_current_user
from backend.models import User
from backend.schemas import (
    PurchaseOrderCreate, PurchaseOrderUpdate,
    PurchaseOrderResponse, PurchaseOrderListResponse, DashboardStats,
)
from backend import crud
from backend.services.po_service import create_purchase_order

router = APIRouter(prefix="/api/purchase-orders", tags=["Purchase Orders"])


@router.get("/stats", response_model=DashboardStats)
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get aggregated dashboard statistics."""
    try:
        return crud.get_dashboard_stats(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[PurchaseOrderListResponse])
def list_purchase_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve purchase orders with optional filters."""
    try:
        return crud.get_purchase_orders(db, skip=skip, limit=limit, status=status, search=search)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{po_id}", response_model=PurchaseOrderResponse)
def get_purchase_order(
    po_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve a single purchase order with all details."""
    try:
        po = crud.get_purchase_order(db, po_id)
        if not po:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        return po
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=PurchaseOrderResponse, status_code=201)
def create_po(
    po_data: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new purchase order with line items."""
    try:
        items = [item.model_dump() for item in po_data.items]
        po = create_purchase_order(
            db,
            vendor_id=po_data.vendor_id,
            items=items,
            notes=po_data.notes,
            created_by=current_user.user_id,
        )
        return po
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{po_id}/status", response_model=PurchaseOrderResponse)
def update_po_status(
    po_id: int,
    update: PurchaseOrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update the status of a purchase order."""
    try:
        po = crud.update_po_status(db, po_id, update.status)
        if not po:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        return po
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
