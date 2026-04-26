"""
ERP PO Management System — CRUD Operations
Database access layer for all entities.
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import Optional, List
from decimal import Decimal, ROUND_HALF_UP

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

def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    expiry_before: Optional[str] = None,
) -> List[Product]:
    """Retrieve products with optional search and grocery-specific filters."""
    query = db.query(Product).filter(Product.is_active == True)
    if search:
        query = query.filter(
            (Product.name.ilike(f"%{search}%")) | (Product.sku.ilike(f"%{search}%"))
        )
    if category:
        query = query.filter(Product.category == category)
    if brand:
        query = query.filter(Product.brand == brand)
    if expiry_before:
        query = query.filter(Product.expiry_date <= expiry_before)

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
        quantity = int(item["quantity"])
        unit_price = Decimal(str(item["unit_price"]))
        gst_rate = Decimal(str(item.get("gst_rate", "5.00")))
        line_total = (Decimal(quantity) * unit_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        tax_amount = (line_total * (gst_rate / Decimal("100"))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        poi = PurchaseOrderItem(
            po_id=po.po_id,
            product_id=item["product_id"],
            quantity=quantity,
            unit_price=unit_price,
            gst_rate=gst_rate,
            tax_amount=tax_amount,
            line_total=line_total,
        )
        db.add(poi)

        # On PO creation, stock is immediately updated per requested workflow.
        product = get_product(db, item["product_id"])
        if product:
            product.stock_level = (product.stock_level or 0) + quantity

    po.stock_updated = True

    db.commit()
    db.refresh(po)
    po_full = get_purchase_order(db, po.po_id)
    po_full.low_stock_alerts = get_low_stock_alerts(db)
    return po_full


def update_po_status(db: Session, po_id: int, new_status: str) -> Optional[PurchaseOrder]:
    """Update a PO's status."""
    po = db.query(PurchaseOrder).filter(PurchaseOrder.po_id == po_id).first()
    if not po:
        return None

    # Backward-compatible safeguard for old records where stock was not updated at creation.
    if new_status == "Received" and not po.stock_updated:
        items = db.query(PurchaseOrderItem).filter(PurchaseOrderItem.po_id == po.po_id).all()
        for item in items:
            product = get_product(db, item.product_id)
            if product:
                product.stock_level = (product.stock_level or 0) + (item.quantity or 0)
        po.stock_updated = True

    po.status = new_status
    db.commit()
    po_full = get_purchase_order(db, po_id)
    po_full.low_stock_alerts = get_low_stock_alerts(db)
    return po_full


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
    low_stock_products = (
        db.query(Product)
        .filter(Product.is_active == True, Product.stock_level < Product.minimum_stock)
        .order_by(Product.stock_level.asc(), Product.name.asc())
        .limit(20)
        .all()
    )

    return {
        "total_pos": total,
        "pending_pos": pending,
        "approved_pos": approved,
        "rejected_pos": rejected,
        "completed_pos": completed,
        "total_vendors": vendors,
        "total_products": products,
        "total_value": total_value,
        "low_stock_products": low_stock_products,
    }


def get_low_stock_products(db: Session, limit: int = 50) -> List[Product]:
    """Get active products currently below minimum stock threshold."""
    return (
        db.query(Product)
        .filter(Product.is_active == True, Product.stock_level < Product.minimum_stock)
        .order_by(Product.stock_level.asc(), Product.name.asc())
        .limit(limit)
        .all()
    )


def get_low_stock_alerts(db: Session, limit: int = 10) -> List[str]:
    """Generate human-readable low-stock warnings for API responses."""
    alerts = []
    for product in get_low_stock_products(db, limit=limit):
        alerts.append(
            f"Low Stock Alert: {product.name} (stock {product.stock_level}, minimum {product.minimum_stock})"
        )
    return alerts
