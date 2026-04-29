from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import POItem, PurchaseOrder, Stock, StockBatch, StockMovement, User, Vendor


router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/stock-valuation")
def stock_valuation(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    items = (
        db.query(
            Stock.product_id,
            func.sum(Stock.current_qty).label("qty"),
            func.avg(POItem.unit_price).label("avg_cost"),
        )
        .outerjoin(POItem, POItem.product_id == Stock.product_id)
        .group_by(Stock.product_id)
        .all()
    )

    rows = []
    total_value = 0.0
    for i in items:
        qty = float(i.qty or 0)
        avg_cost = float(i.avg_cost or 0)
        value = round(qty * avg_cost, 2)
        total_value += value
        rows.append({"product_id": i.product_id, "qty": qty, "avg_cost": avg_cost, "value": value})

    return {"report": "stock_valuation", "total_value": round(total_value, 2), "items": rows}


@router.get("/expiry-analysis")
def expiry_analysis(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    today = date.today()
    d7 = today + timedelta(days=7)
    d30 = today + timedelta(days=30)

    expired = db.query(StockBatch).filter(StockBatch.expiry_date.is_not(None), StockBatch.expiry_date < today).count()
    critical = db.query(StockBatch).filter(StockBatch.expiry_date.is_not(None), StockBatch.expiry_date >= today, StockBatch.expiry_date <= d7).count()
    warning = db.query(StockBatch).filter(StockBatch.expiry_date.is_not(None), StockBatch.expiry_date > d7, StockBatch.expiry_date <= d30).count()

    return {
        "report": "expiry_analysis",
        "expired": expired,
        "critical_7_days": critical,
        "warning_30_days": warning,
    }


@router.get("/vendor-performance")
def vendor_performance(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    rows = (
        db.query(
            Vendor.id,
            Vendor.name,
            func.count(PurchaseOrder.id).label("po_count"),
            func.sum(PurchaseOrder.total_amount).label("total_spend"),
        )
        .outerjoin(PurchaseOrder, PurchaseOrder.vendor_id == Vendor.id)
        .group_by(Vendor.id, Vendor.name)
        .all()
    )

    return {
        "report": "vendor_performance",
        "items": [
            {
                "vendor_id": r.id,
                "vendor_name": r.name,
                "po_count": int(r.po_count or 0),
                "total_spend": float(r.total_spend or 0),
            }
            for r in rows
        ],
    }


@router.get("/purchase-history")
def purchase_history(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    rows = db.query(PurchaseOrder).order_by(PurchaseOrder.order_date.desc()).limit(200).all()
    return {
        "report": "purchase_history",
        "items": [
            {
                "id": r.id,
                "po_number": r.po_number,
                "status": r.status.value,
                "vendor_id": r.vendor_id,
                "order_date": r.order_date,
                "total_amount": float(r.total_amount),
            }
            for r in rows
        ],
    }


@router.get("/low-stock")
def report_low_stock(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    rows = db.query(Stock).filter(Stock.current_qty <= Stock.reorder_level).all()
    return {
        "report": "low_stock",
        "items": [
            {
                "stock_id": s.id,
                "product_id": s.product_id,
                "warehouse_location": s.warehouse_location,
                "current_qty": float(s.current_qty),
                "reorder_level": float(s.reorder_level),
            }
            for s in rows
        ],
    }


@router.get("/stock-movement")
def stock_movement_audit(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    rows = db.query(StockMovement).order_by(StockMovement.created_at.desc()).limit(200).all()
    return {
        "report": "stock_movement",
        "items": [
            {
                "id": row.id,
                "product_id": row.product_id,
                "batch_id": row.batch_id,
                "movement_type": row.movement_type.value,
                "quantity": float(row.quantity),
                "reference_id": row.reference_id,
                "reference_type": row.reference_type,
                "notes": row.notes,
                "created_by": row.created_by,
                "created_at": row.created_at,
            }
            for row in rows
        ],
    }
