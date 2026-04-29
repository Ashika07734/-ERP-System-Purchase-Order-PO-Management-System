from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Product, Stock, StockBatch, User
from app.schemas import ProductCreate, ProductRead, ProductUpdate, StockRead


router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
def list_products(
    category: str | None = None,
    perishable: bool | None = None,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    if perishable is not None:
        query = query.filter(Product.is_perishable == perishable)
    return query.order_by(Product.id.desc()).all()


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    existing = db.query(Product).filter(Product.sku == payload.sku).first()
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")

    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    stock_rows = db.query(Stock).filter(Stock.product_id == product_id).all()
    batches = (
        db.query(StockBatch)
        .filter(StockBatch.product_id == product_id)
        .order_by(StockBatch.expiry_date.asc().nullslast(), StockBatch.created_at.desc())
        .all()
    )

    return {
        "product": ProductRead.model_validate(product).model_dump(),
        "stock": [StockRead.model_validate(row).model_dump() for row in stock_rows],
        "batches": [
            {
                "id": b.id,
                "batch_number": b.batch_number,
                "received_date": b.received_date,
                "expiry_date": b.expiry_date,
                "quantity": float(b.quantity),
                "remaining_qty": float(b.remaining_qty),
                "status": b.status.value,
            }
            for b in batches
        ],
    }


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.get("/{product_id}/stock", response_model=list[StockRead])
def product_stock(
    product_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return db.query(Stock).filter(Stock.product_id == product_id).all()


@router.get("/{product_id}/batches")
def product_batches(
    product_id: int,
    days: int | None = Query(default=None, ge=1, le=365),
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    query = db.query(StockBatch).filter(StockBatch.product_id == product_id)
    if days is not None:
        from datetime import date, timedelta

        limit = date.today() + timedelta(days=days)
        query = query.filter(StockBatch.expiry_date.is_not(None), StockBatch.expiry_date <= limit)

    rows = query.order_by(StockBatch.expiry_date.asc().nullslast()).all()
    return [
        {
            "id": row.id,
            "batch_number": row.batch_number,
            "received_date": row.received_date,
            "expiry_date": row.expiry_date,
            "quantity": float(row.quantity),
            "remaining_qty": float(row.remaining_qty),
            "status": row.status.value,
        }
        for row in rows
    ]
