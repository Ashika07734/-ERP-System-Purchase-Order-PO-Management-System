from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Alert, AlertType, MovementType, POItem, POStatus, Product, PurchaseOrder, Stock, StockBatch, StockMovement, User, Vendor
from app.schemas import POCreate, PORead, POReceiveRequest, POUpdate


router = APIRouter(prefix="/purchase-orders", tags=["purchase-orders"])


def _generate_po_number(db: Session) -> str:
    today = date.today()
    prefix = f"PO-{today.year}-"
    count = db.query(PurchaseOrder).filter(PurchaseOrder.po_number.like(f"{prefix}%")).count() + 1
    return f"{prefix}{count:04d}"


def _compute_line_total(ordered_qty: float, unit_price: float, tax_rate: float, discount_pct: float) -> float:
    base = ordered_qty * unit_price
    taxed = base + (base * (tax_rate / 100.0))
    discounted = taxed - (taxed * (discount_pct / 100.0))
    return round(discounted, 2)


def _recompute_totals(db: Session, po: PurchaseOrder) -> None:
    items = db.query(POItem).filter(POItem.po_id == po.id).all()
    subtotal = sum(float(i.ordered_qty) * float(i.unit_price) for i in items)
    gross = sum(float(i.line_total or 0) for i in items)
    tax = sum((float(i.ordered_qty) * float(i.unit_price)) * (float(i.tax_rate) / 100.0) for i in items)
    discount = gross - (subtotal + tax)

    po.subtotal = round(subtotal, 2)
    po.tax_amount = round(tax, 2)
    po.discount_amount = round(abs(discount), 2)
    po.total_amount = round(gross, 2)


@router.get("", response_model=list[PORead])
def list_purchase_orders(
    status: POStatus | None = None,
    vendor_id: int | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    query = db.query(PurchaseOrder)
    if status is not None:
        query = query.filter(PurchaseOrder.status == status)
    if vendor_id is not None:
        query = query.filter(PurchaseOrder.vendor_id == vendor_id)

    return query.order_by(PurchaseOrder.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()


@router.post("", response_model=PORead, status_code=status.HTTP_201_CREATED)
def create_purchase_order(
    payload: POCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    vendor = db.query(Vendor).filter(Vendor.id == payload.vendor_id, Vendor.is_deleted.is_(False)).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    if not payload.items:
        raise HTTPException(status_code=400, detail="At least one line item is required")

    po = PurchaseOrder(
        po_number=_generate_po_number(db),
        vendor_id=payload.vendor_id,
        created_by=user.id,
        expected_date=payload.expected_date,
        notes=payload.notes,
        shipping_address=payload.shipping_address,
        status=POStatus.draft,
    )
    db.add(po)
    db.flush()

    for item in payload.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        line_total = _compute_line_total(item.ordered_qty, item.unit_price, item.tax_rate, item.discount_pct)
        po_item = POItem(
            po_id=po.id,
            product_id=item.product_id,
            vendor_sku=item.vendor_sku,
            description=item.description,
            ordered_qty=item.ordered_qty,
            unit_price=item.unit_price,
            tax_rate=item.tax_rate,
            discount_pct=item.discount_pct,
            line_total=line_total,
            expiry_date=item.expiry_date,
            notes=item.notes,
        )
        db.add(po_item)

    _recompute_totals(db, po)
    db.commit()
    db.refresh(po)
    return po


@router.get("/{po_id}")
def get_purchase_order(
    po_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="PO not found")

    items = db.query(POItem).filter(POItem.po_id == po_id).all()
    return {
        "po": PORead.model_validate(po).model_dump(),
        "items": [
            {
                "id": i.id,
                "product_id": i.product_id,
                "ordered_qty": float(i.ordered_qty),
                "received_qty": float(i.received_qty),
                "unit_price": float(i.unit_price),
                "tax_rate": float(i.tax_rate),
                "discount_pct": float(i.discount_pct),
                "line_total": float(i.line_total or 0),
                "expiry_date": i.expiry_date,
            }
            for i in items
        ],
    }


@router.put("/{po_id}", response_model=PORead)
def update_purchase_order(
    po_id: int,
    payload: POUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="PO not found")
    if po.status != POStatus.draft:
        raise HTTPException(status_code=400, detail="Only draft POs can be updated")

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(po, key, value)

    db.commit()
    db.refresh(po)
    return po


@router.post("/{po_id}/approve")
def approve_purchase_order(
    po_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="PO not found")
    if po.status not in {POStatus.draft, POStatus.pending_approval}:
        raise HTTPException(status_code=400, detail="PO cannot be approved in current state")

    po.status = POStatus.approved
    po.approved_by = user.id
    db.commit()
    return {"id": po_id, "status": po.status.value}


@router.post("/{po_id}/send")
def send_purchase_order(
    po_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="PO not found")
    if po.status != POStatus.approved:
        raise HTTPException(status_code=400, detail="PO must be approved before sending")

    po.status = POStatus.sent
    db.commit()
    return {"id": po_id, "status": po.status.value}


@router.post("/{po_id}/receive")
def receive_purchase_order(
    po_id: int,
    payload: POReceiveRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="PO not found")
    if po.status not in {POStatus.sent, POStatus.partially_received}:
        raise HTTPException(status_code=400, detail="PO must be sent before receiving")

    items = db.query(POItem).filter(POItem.po_id == po_id).all()
    item_map = {item.id: item for item in items}

    for row in payload.items:
        po_item = item_map.get(row.po_item_id)
        if not po_item:
            raise HTTPException(status_code=404, detail=f"PO item {row.po_item_id} not found")

        po_item.received_qty = float(po_item.received_qty) + row.received_qty

        batch = StockBatch(
            product_id=po_item.product_id,
            batch_number=row.batch_number,
            received_date=payload.received_date,
            expiry_date=row.expiry_date,
            quantity=row.received_qty,
            remaining_qty=row.received_qty,
            cost_price=po_item.unit_price,
            po_id=po.id,
        )
        db.add(batch)
        db.flush()

        stock = db.query(Stock).filter(Stock.product_id == po_item.product_id, Stock.warehouse_location == "MAIN").first()
        if not stock:
            stock = Stock(
                product_id=po_item.product_id,
                warehouse_location="MAIN",
                current_qty=0,
                reorder_level=0,
                reorder_qty=0,
            )
            db.add(stock)
            db.flush()

        stock.current_qty = float(stock.current_qty) + row.received_qty

        move = StockMovement(
            product_id=po_item.product_id,
            batch_id=batch.id,
            movement_type=MovementType.receipt,
            quantity=row.received_qty,
            reference_id=po.id,
            reference_type="purchase_order",
            notes=f"PO receipt {po.po_number}",
            created_by=user.id,
        )
        db.add(move)

    all_received = all(float(item.received_qty) >= float(item.ordered_qty) for item in items)
    po.status = POStatus.received if all_received else POStatus.partially_received
    po.received_date = payload.received_date

    if po.status == POStatus.partially_received:
        db.add(
            Alert(
                type=AlertType.po_overdue,
                message=f"PO {po.po_number} partially received.",
            )
        )

    db.commit()
    return {"id": po_id, "status": po.status.value}


@router.get("/{po_id}/pdf", response_class=HTMLResponse)
def purchase_order_pdf(
    po_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="PO not found")

    items = db.query(POItem).filter(POItem.po_id == po_id).all()
    row_html = "".join(
        (
            "<tr>"
            f"<td>{item.product_id}</td>"
            f"<td>{float(item.ordered_qty):.3f}</td>"
            f"<td>{float(item.received_qty):.3f}</td>"
            f"<td>{float(item.unit_price):.2f}</td>"
            f"<td>{float(item.line_total or 0):.2f}</td>"
            "</tr>"
        )
        for item in items
    )

    html = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset=\"utf-8\" />
      <title>PO {po.po_number}</title>
      <style>
        body {{ font-family: Arial, sans-serif; margin: 24px; }}
        h1 {{ margin-bottom: 8px; }}
        .meta {{ margin-bottom: 16px; color: #333; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #f5f5f5; }}
        .totals {{ margin-top: 12px; font-weight: bold; }}
      </style>
    </head>
    <body>
      <h1>Purchase Order {po.po_number}</h1>
      <div class=\"meta\">Status: {po.status.value} | Vendor ID: {po.vendor_id or '-'} | Order Date: {po.order_date}</div>
      <table>
        <thead>
          <tr>
            <th>Product ID</th>
            <th>Ordered Qty</th>
            <th>Received Qty</th>
            <th>Unit Price</th>
            <th>Line Total</th>
          </tr>
        </thead>
        <tbody>{row_html}</tbody>
      </table>
      <div class=\"totals\">Subtotal: {float(po.subtotal):.2f} | Tax: {float(po.tax_amount):.2f} | Discount: {float(po.discount_amount):.2f} | Total: {float(po.total_amount):.2f}</div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
