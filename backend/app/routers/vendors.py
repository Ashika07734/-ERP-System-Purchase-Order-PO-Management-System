from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import POItem, Product, PurchaseOrder, User, Vendor
from app.schemas import VendorCreate, VendorRead, VendorUpdate


router = APIRouter(prefix="/vendors", tags=["vendors"])


@router.get("", response_model=list[VendorRead])
def list_vendors(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    query = db.query(Vendor).filter(Vendor.is_deleted.is_(False))
    if search:
        like = f"%{search}%"
        query = query.filter(Vendor.name.ilike(like))

    return query.order_by(Vendor.id.desc()).offset((page - 1) * page_size).limit(page_size).all()


@router.post("", response_model=VendorRead, status_code=status.HTTP_201_CREATED)
def create_vendor(
    payload: VendorCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    vendor = Vendor(**payload.model_dump())
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor


@router.get("/{vendor_id}")
def get_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id, Vendor.is_deleted.is_(False)).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    recent_products = (
        db.query(Product.id, Product.name, Product.sku)
        .join(POItem, POItem.product_id == Product.id)
        .join(PurchaseOrder, PurchaseOrder.id == POItem.po_id)
        .filter(PurchaseOrder.vendor_id == vendor_id)
        .distinct()
        .limit(20)
        .all()
    )

    return {
        "vendor": VendorRead.model_validate(vendor).model_dump(),
        "products": [
            {"id": row.id, "name": row.name, "sku": row.sku}
            for row in recent_products
        ],
    }


@router.put("/{vendor_id}", response_model=VendorRead)
def update_vendor(
    vendor_id: int,
    payload: VendorUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id, Vendor.is_deleted.is_(False)).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(vendor, key, value)

    db.commit()
    db.refresh(vendor)
    return vendor


@router.delete("/{vendor_id}")
def delete_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id, Vendor.is_deleted.is_(False)).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    vendor.is_deleted = True
    db.commit()
    return {"vendor_id": vendor_id, "deleted": True, "mode": "soft"}


@router.get("/{vendor_id}/pos")
def vendor_pos(
    vendor_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    rows = (
        db.query(PurchaseOrder)
        .filter(PurchaseOrder.vendor_id == vendor_id)
        .order_by(PurchaseOrder.created_at.desc())
        .all()
    )
    return {
        "vendor_id": vendor_id,
        "purchase_orders": [
            {
                "id": po.id,
                "po_number": po.po_number,
                "status": po.status.value,
                "total_amount": float(po.total_amount),
                "order_date": po.order_date,
            }
            for po in rows
        ],
    }
