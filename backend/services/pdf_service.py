"""
ERP PO Management System — PDF Service
Generate printable purchase order documents.
"""

from io import BytesIO
from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def _safe_decimal(value) -> Decimal:
    if value is None:
        return Decimal("0.00")
    return Decimal(str(value))


def generate_purchase_order_pdf(po):
    """Generate a purchase-order PDF and return an in-memory byte stream."""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 20 * mm

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(20 * mm, y, "Purchase Order")

    y -= 10 * mm
    pdf.setFont("Helvetica", 10)
    pdf.drawString(20 * mm, y, f"Reference: {po.reference_no}")
    pdf.drawRightString(width - 20 * mm, y, f"Date: {po.created_at.strftime('%Y-%m-%d')}")

    y -= 8 * mm
    vendor_name = po.vendor.name if po.vendor else "N/A"
    vendor_gst = po.vendor.gst_number if po.vendor and po.vendor.gst_number else "N/A"
    pdf.drawString(20 * mm, y, f"Vendor: {vendor_name}")

    y -= 6 * mm
    pdf.drawString(20 * mm, y, f"GST Number: {vendor_gst}")

    y -= 10 * mm
    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(0.8)
    pdf.line(20 * mm, y, width - 20 * mm, y)

    y -= 8 * mm
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(20 * mm, y, "Product")
    pdf.drawString(75 * mm, y, "Qty")
    pdf.drawString(90 * mm, y, "Unit")
    pdf.drawString(110 * mm, y, "Price")
    pdf.drawString(130 * mm, y, "Tax")
    pdf.drawRightString(width - 20 * mm, y, "Total")

    y -= 4 * mm
    pdf.line(20 * mm, y, width - 20 * mm, y)
    y -= 6 * mm

    pdf.setFont("Helvetica", 9)

    for item in po.items:
        if y < 30 * mm:
            pdf.showPage()
            y = height - 20 * mm
            pdf.setFont("Helvetica", 9)

        product_name = item.product.name if item.product else f"Product #{item.product_id}"
        unit_type = item.product.unit_type if item.product and item.product.unit_type else "Unit"
        line_total = _safe_decimal(item.line_total)
        tax_amount = _safe_decimal(item.tax_amount)

        pdf.drawString(20 * mm, y, product_name[:34])
        pdf.drawString(75 * mm, y, str(item.quantity))
        pdf.drawString(90 * mm, y, unit_type)
        pdf.drawString(110 * mm, y, f"{_safe_decimal(item.unit_price):.2f}")
        pdf.drawString(130 * mm, y, f"{tax_amount:.2f}")
        pdf.drawRightString(width - 20 * mm, y, f"{line_total:.2f}")
        y -= 6 * mm

    y -= 4 * mm
    pdf.line(20 * mm, y, width - 20 * mm, y)

    y -= 8 * mm
    subtotal = _safe_decimal(po.subtotal)
    tax_total = _safe_decimal(po.tax_amount)
    grand_total = _safe_decimal(po.total_amount)

    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(width - 45 * mm, y, "Subtotal:")
    pdf.drawRightString(width - 20 * mm, y, f"{subtotal:.2f}")

    y -= 6 * mm
    pdf.drawRightString(width - 45 * mm, y, "Tax:")
    pdf.drawRightString(width - 20 * mm, y, f"{tax_total:.2f}")

    y -= 7 * mm
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawRightString(width - 45 * mm, y, "Total:")
    pdf.drawRightString(width - 20 * mm, y, f"{grand_total:.2f}")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer
