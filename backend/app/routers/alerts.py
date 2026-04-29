from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Alert, AlertType, BatchStatus, Stock, StockBatch, User
from app.schemas import AlertRead


router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertRead])
def list_alerts(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return (
        db.query(Alert)
        .filter(Alert.is_resolved.is_(False))
        .order_by(Alert.created_at.desc())
        .all()
    )


@router.put("/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.is_resolved = True
    db.commit()
    return {"id": alert_id, "resolved": True}


@router.put("/read-all")
def read_all_alerts(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    db.query(Alert).filter(Alert.is_read.is_(False)).update({"is_read": True})
    db.commit()
    return {"updated": True, "message": "All alerts marked read"}


@router.post("/trigger")
def trigger_alert_check(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    today = date.today()
    warn_30 = today + timedelta(days=30)
    warn_7 = today + timedelta(days=7)

    created = 0

    low_stock_rows = db.query(Stock).filter(Stock.current_qty <= Stock.reorder_level).all()
    for row in low_stock_rows:
        exists = (
            db.query(Alert)
            .filter(
                Alert.type == AlertType.low_stock,
                Alert.product_id == row.product_id,
                Alert.is_resolved.is_(False),
            )
            .first()
        )
        if not exists:
            db.add(
                Alert(
                    type=AlertType.low_stock,
                    product_id=row.product_id,
                    message=(
                        f"Low stock for product #{row.product_id}: "
                        f"{float(row.current_qty)} <= reorder {float(row.reorder_level)}"
                    ),
                )
            )
            created += 1

    batches = db.query(StockBatch).filter(StockBatch.expiry_date.is_not(None), StockBatch.remaining_qty > 0).all()
    for batch in batches:
        if batch.expiry_date is None:
            continue

        if batch.expiry_date < today:
            alert_type = AlertType.expired
            batch.status = BatchStatus.expired
        elif batch.expiry_date <= warn_7:
            alert_type = AlertType.expiry_critical
        elif batch.expiry_date <= warn_30:
            alert_type = AlertType.expiry_warning
        else:
            continue

        exists = (
            db.query(Alert)
            .filter(
                Alert.type == alert_type,
                Alert.batch_id == batch.id,
                Alert.is_resolved.is_(False),
            )
            .first()
        )
        if not exists:
            db.add(
                Alert(
                    type=alert_type,
                    product_id=batch.product_id,
                    batch_id=batch.id,
                    message=(
                        f"Batch {batch.batch_number} for product #{batch.product_id} "
                        f"expires on {batch.expiry_date}."
                    ),
                )
            )
            created += 1

    db.commit()
    return {"queued": True, "created_alerts": created}
