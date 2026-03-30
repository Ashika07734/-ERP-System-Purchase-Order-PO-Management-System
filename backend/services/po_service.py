"""
ERP PO Management System — Purchase Order Service
Business logic: tax calculation, total computation, PO creation orchestration.
"""

from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import Session

from backend import crud
from backend.utils import generate_reference_no

# Tax rate constant
TAX_RATE = Decimal("0.05")  # 5%


def calculate_total(items: list) -> dict:
    """
    Calculate subtotal, tax, and total for a list of PO items.

    Args:
        items: list of dicts with 'quantity' and 'unit_price' keys.

    Returns:
        dict with 'subtotal', 'tax_amount', 'total_amount'.

    Business rule:
        total = subtotal + (subtotal * 0.05)
    """
    subtotal = Decimal("0.00")
    for item in items:
        qty = Decimal(str(item["quantity"]))
        price = Decimal(str(item["unit_price"]))
        subtotal += (qty * price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    tax_amount = (subtotal * TAX_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
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
        items_data.append({
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "unit_price": item["unit_price"],
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
