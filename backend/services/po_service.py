"""
ERP PO Management System — Purchase Order Service
Business logic: tax calculation, total computation, PO creation orchestration.
"""

from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import Session

from backend import crud
from backend.utils import generate_reference_no

def calculate_total(items: list) -> dict:
    """
    Calculate subtotal, tax, and total for a list of PO items with per-item GST.

    Args:
        items: list of dicts with 'quantity', 'unit_price', and optional 'gst_rate' keys.

    Returns:
        dict with 'subtotal', 'tax_amount', 'total_amount'.

    Business rule:
        tax per line = line_total * gst_rate / 100
        total = subtotal + sum(line taxes)
    """
    subtotal = Decimal("0.00")
    tax_amount = Decimal("0.00")
    for item in items:
        qty = Decimal(str(item["quantity"]))
        price = Decimal(str(item["unit_price"]))
        gst_rate = Decimal(str(item.get("gst_rate", "5.00")))
        line_total = (qty * price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        line_tax = (line_total * (gst_rate / Decimal("100"))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        subtotal += line_total
        tax_amount += line_tax

    total_amount = subtotal + tax_amount

    return {
        "subtotal": subtotal,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
    }


def create_purchase_order(db: Session, vendor_id: int, items: list, notes: str = None, created_by: int = None):
    """
    Orchestrate the full PO creation process:
      1. Validate vendor exists
      2. Calculate totals with tax
      3. Generate unique reference number
      4. Persist PO and items
    """
    # 1. Validate vendor
    vendor = crud.get_vendor(db, vendor_id)
    if not vendor:
        raise ValueError(f"Vendor with ID {vendor_id} not found")

    # 2. Validate products exist and build items
    items_data = []
    for item in items:
        product = crud.get_product(db, item["product_id"])
        if not product:
            raise ValueError(f"Product with ID {item['product_id']} not found")

        gst_rate = item.get("gst_rate")
        if gst_rate is None:
            gst_rate = str(product.gst_rate or "5.00")

        items_data.append({
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "unit_price": item["unit_price"],
            "gst_rate": gst_rate,
        })

    # 3. Calculate totals
    totals = calculate_total(items_data)

    # 4. Generate reference number
    count = crud.get_po_count(db)
    reference_no = generate_reference_no(count)

    # 5. Build PO data and persist
    po_data = {
        "reference_no": reference_no,
        "vendor_id": vendor_id,
        "subtotal": totals["subtotal"],
        "tax_amount": totals["tax_amount"],
        "total_amount": totals["total_amount"],
        "status": "Pending",
        "notes": notes,
        "created_by": created_by,
    }

    return crud.create_purchase_order(db, po_data, items_data)
