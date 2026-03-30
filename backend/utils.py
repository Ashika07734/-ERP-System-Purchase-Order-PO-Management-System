"""
ERP PO Management System — Utility Helpers
Reference number generation, date formatting, and error utilities.
"""

from datetime import datetime


def generate_reference_no(count: int) -> str:
    """Generate a unique PO reference number like PO-2026-00008."""
    year = datetime.now().year
    seq = count + 1
    return f"PO-{year}-{seq:05d}"


def format_currency(amount) -> str:
    """Format a decimal as currency string."""
    return f"${float(amount):,.2f}"


def error_response(message: str, details: str = None) -> dict:
    """Build a standardized error response dict."""
    resp = {"error": True, "message": message}
    if details:
        resp["details"] = details
    return resp
