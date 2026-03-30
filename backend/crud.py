"""
ERP PO Management System — CRUD Operations
Database access layer for all entities.
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import Optional, List

from backend.models import Vendor, Product, PurchaseOrder, PurchaseOrderItem


# ══════════════════════════════════════════════════════════
# VENDOR CRUD
# ══════════════════════════════════════════════════════════

def get_vendors(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[Vendor]:
    """Retrieve vendors with optional search."""
    query = db.query(Vendor).filter(Vendor.is_active == True)
    if search:
        query = query.filter(Vendor.name.ilike(f"%{search}%"))
    return query.order_by(Vendor.name).offset(skip).limit(limit).all()


def get_vendor(db: Session, vendor_id: int) -> Optional[Vendor]:
    """Retrieve a single vendor by ID."""
    return db.query(Vendor).filter(Vendor.vendor_id == vendor_id, Vendor.is_active == True).first()


def create_vendor(db: Session, vendor_data: dict) -> Vendor:
    """Create a new vendor."""
    vendor = Vendor(**vendor_data)
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor


def update_vendor(db: Session, vendor_id: int, vendor_data: dict) -> Optional[Vendor]:
    """Update an existing vendor."""
    vendor = get_vendor(db, vendor_id)
    if not vendor:
        return None
    for key, value in vendor_data.items():
        if value is not None:
            setattr(vendor, key, value)
    db.commit()
    db.refresh(vendor)
    return vendor


def delete_vendor(db: Session, vendor_id: int) -> bool:
    """Soft-delete a vendor."""
    vendor = get_vendor(db, vendor_id)
    if not vendor:
        return False
    vendor.is_active = False
    db.commit()
    return True


# ══════════════════════════════════════════════════════════
# PRODUCT CRUD
# ══════════════════════════════════════════════════════════

def get_products(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None, category: Optional[str] = None) -> List[Product]:
    """Retrieve products with optional search and category filter."""
    query = db.query(Product).filter(Product.is_active == True)
    if search:
        query = query.filter(
            (Product.name.ilike(f"%{search}%")) | (Product.sku.ilike(f"%{search}%"))
        )
    if category:
        query = query.filter(Product.category == category)
    return query.order_by(Product.name).offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int) -> Optional[Product]:
    """Retrieve a single product by ID."""
    return db.query(Product).filter(Product.product_id == product_id, Product.is_active == True).first()


def create_product(db: Session, product_data: dict) -> Product:
    """Create a new product."""
    product = Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, product_data: dict) -> Optional[Product]:
    """Update an existing product."""
    product = get_product(db, product_id)
    if not product:
        return None
    for key, value in product_data.items():
        if value is not None:
            setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> bool:
    """Soft-delete a product."""
    product = get_product(db, product_id)
    if not product:
        return False
    product.is_active = False
    db.commit()
    return True


# ══════════════════════════════════════════════════════════
# PURCHASE ORDER CRUD
# ══════════════════════════════════════════════════════════

def get_purchase_orders(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    search: Optional[str] = None,
) -> List[PurchaseOrder]:
    """Retrieve POs with optional status filter and search."""
    query = db.query(PurchaseOrder).options(joinedload(PurchaseOrder.vendor))
    if status:
        query = query.filter(PurchaseOrder.status == status)
    if search:
        query = query.filter(PurchaseOrder.reference_no.ilike(f"%{search}%"))
    return query.order_by(desc(PurchaseOrder.created_at)).offset(skip).limit(limit).all()


def get_purchase_order(db: Session, po_id: int) -> Optional[PurchaseOrder]:
    """Retrieve a single PO with all related data."""
    return (
        db.query(PurchaseOrder)
        .options(
            joinedload(PurchaseOrder.vendor),
            joinedload(PurchaseOrder.items).joinedload(PurchaseOrderItem.product),
        )
        .filter(PurchaseOrder.po_id == po_id)
        .first()
    )


def create_purchase_order(db: Session, po_data: dict, items_data: list) -> PurchaseOrder:
    """Create a PO with its line items."""
    po = PurchaseOrder(**po_data)
    db.add(po)
    db.flush()  # Get po_id

    for item in items_data:
        line_total = item["quantity"] * float(item["unit_price"])
        poi = PurchaseOrderItem(po_id=po.po_id, line_total=line_total, **item)
        db.add(poi)

    db.commit()
    db.refresh(po)
    return get_purchase_order(db, po.po_id)


def update_po_status(db: Session, po_id: int, new_status: str) -> Optional[PurchaseOrder]:
    """Update a PO's status."""
    po = db.query(PurchaseOrder).filter(PurchaseOrder.po_id == po_id).first()
    if not po:
        return None
    po.status = new_status
    db.commit()
    return get_purchase_order(db, po_id)


def get_po_count(db: Session) -> int:
    """Get total PO count (for reference number generation)."""
    return db.query(func.count(PurchaseOrder.po_id)).scalar() or 0


# ══════════════════════════════════════════════════════════
# DASHBOARD STATS
# ══════════════════════════════════════════════════════════

def get_dashboard_stats(db: Session) -> dict:
    """Aggregate dashboard statistics."""
    total = db.query(func.count(PurchaseOrder.po_id)).scalar() or 0
    pending = db.query(func.count(PurchaseOrder.po_id)).filter(PurchaseOrder.status == "Pending").scalar() or 0
    approved = db.query(func.count(PurchaseOrder.po_id)).filter(PurchaseOrder.status == "Approved").scalar() or 0
    rejected = db.query(func.count(PurchaseOrder.po_id)).filter(PurchaseOrder.status == "Rejected").scalar() or 0
    completed = db.query(func.count(PurchaseOrder.po_id)).filter(PurchaseOrder.status == "Completed").scalar() or 0
    total_value = db.query(func.coalesce(func.sum(PurchaseOrder.total_amount), 0)).scalar()
    vendors = db.query(func.count(Vendor.vendor_id)).filter(Vendor.is_active == True).scalar() or 0
    products = db.query(func.count(Product.product_id)).filter(Product.is_active == True).scalar() or 0

    return {
        "total_pos": total,
        "pending_pos": pending,
        "approved_pos": approved,
        "rejected_pos": rejected,
        "completed_pos": completed,
        "total_vendors": vendors,
        "total_products": products,
        "total_value": total_value,
    }
