from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Alert, AlertType, MovementType, Product, Stock, StockBatch, StockMovement, User
from app.schemas import BatchCreateRequest, StockAdjustRequest, StockRead


router = APIRouter(prefix="/stock", tags=["stock"])


def _upsert_low_stock_alert(db: Session, stock_row: Stock) -> None:
    if float(stock_row.current_qty) > float(stock_row.reorder_level):
        return

    existing = (
        db.query(Alert)
        .filter(
            Alert.type == AlertType.low_stock,
            Alert.product_id == stock_row.product_id,
            Alert.is_resolved.is_(False),
        )
        .first()
    )
    if existing:
        return

    alert = Alert(
        type=AlertType.low_stock,
        product_id=stock_row.product_id,
        message=(
            f"Low stock for product #{stock_row.product_id} at {stock_row.warehouse_location}: "
            f"{float(stock_row.current_qty)} <= reorder {float(stock_row.reorder_level)}"
        ),
    )
    db.add(alert)


@router.get("", response_model=list[StockRead])
def list_stock(
    filter_mode: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    query = db.query(Stock)
    if filter_mode == "low":
        query = query.filter(Stock.current_qty <= Stock.reorder_level)
    elif filter_mode == "critical":
        query = query.filter(Stock.current_qty <= (Stock.reorder_level * 0.5))

    return query.order_by(Stock.last_updated.desc()).all()


@router.get("/low-stock")
def low_stock(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    rows = db.query(Stock).filter(Stock.current_qty <= Stock.reorder_level).all()
    return {
        "items": [
            {
                "stock_id": row.id,
                "product_id": row.product_id,
                "warehouse_location": row.warehouse_location,
                "current_qty": float(row.current_qty),
                "reorder_level": float(row.reorder_level),
            }
            for row in rows
        ],
        "type": "low_stock",
    }


@router.get("/expiring")
def expiring_stock(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    limit = date.today() + timedelta(days=days)
    rows = (
        db.query(StockBatch)
        .filter(
            StockBatch.expiry_date.is_not(None),
            StockBatch.expiry_date <= limit,
            StockBatch.remaining_qty > 0,
        )
        .order_by(StockBatch.expiry_date.asc())
        .all()
    )
    return {
        "items": [
            {
                "batch_id": row.id,
                "product_id": row.product_id,
                "batch_number": row.batch_number,
                "expiry_date": row.expiry_date,
                "remaining_qty": float(row.remaining_qty),
                "status": row.status.value,
            }
            for row in rows
        ],
        "days": days,
    }


@router.post("/adjust")
def adjust_stock(
    payload: StockAdjustRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    stock_row = (
        db.query(Stock)
        .filter(
            Stock.product_id == payload.product_id,
            Stock.warehouse_location == payload.warehouse_location,
        )
        .first()
    )
    if not stock_row:
        stock_row = Stock(
            product_id=payload.product_id,
            warehouse_location=payload.warehouse_location,
            current_qty=0,
            reorder_level=0,
            reorder_qty=0,
        )
        db.add(stock_row)
        db.flush()

    stock_row.current_qty = float(stock_row.current_qty) + payload.quantity_delta

    movement = StockMovement(
        product_id=payload.product_id,
        movement_type=MovementType.adjustment,
        quantity=payload.quantity_delta,
        reference_id=stock_row.id,
        reference_type="stock_adjustment",
        notes=payload.notes,
        created_by=user.id,
    )
    db.add(movement)

    _upsert_low_stock_alert(db, stock_row)
    db.commit()

    return {
        "message": "Stock adjusted",
        "stock_id": stock_row.id,
        "current_qty": float(stock_row.current_qty),
    }


@router.post("/batches")
def add_batch(
    payload: BatchCreateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    batch = StockBatch(
        product_id=payload.product_id,
        batch_number=payload.batch_number,
        received_date=payload.received_date,
        expiry_date=payload.expiry_date,
        quantity=payload.quantity,
        remaining_qty=payload.quantity,
        cost_price=payload.cost_price,
    )
    db.add(batch)

    stock_row = (
        db.query(Stock)
        .filter(
            Stock.product_id == payload.product_id,
            Stock.warehouse_location == payload.warehouse_location,
        )
        .first()
    )
    if not stock_row:
        stock_row = Stock(
            product_id=payload.product_id,
            warehouse_location=payload.warehouse_location,
            current_qty=0,
            reorder_level=0,
            reorder_qty=0,
        )
        db.add(stock_row)
        db.flush()

    stock_row.current_qty = float(stock_row.current_qty) + payload.quantity

    movement = StockMovement(
        product_id=payload.product_id,
        movement_type=MovementType.receipt,
        quantity=payload.quantity,
        reference_id=batch.id,
        reference_type="stock_batch",
        notes="Goods receipt via /stock/batches",
        created_by=user.id,
    )
    db.add(movement)

    _upsert_low_stock_alert(db, stock_row)
    db.commit()
    db.refresh(batch)

    return {
        "message": "Batch added",
        "batch": {
            "id": batch.id,
            "batch_number": batch.batch_number,
            "product_id": batch.product_id,
            "quantity": float(batch.quantity),
            "remaining_qty": float(batch.remaining_qty),
            "expiry_date": batch.expiry_date,
        },
    }
