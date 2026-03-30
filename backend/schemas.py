"""
ERP PO Management System — Pydantic Schemas
Request/response validation models for all API endpoints.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# ── Vendor Schemas ────────────────────────────────────────

class VendorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    contact: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    rating: Optional[Decimal] = Field(default=0.0, ge=0, le=5)

class VendorCreate(VendorBase):
    pass

class VendorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    contact: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    rating: Optional[Decimal] = Field(None, ge=0, le=5)

class VendorResponse(VendorBase):
    vendor_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ── Product Schemas ───────────────────────────────────────

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    sku: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = None
    description: Optional[str] = None
    unit_price: Decimal = Field(..., ge=0)
    stock_level: Optional[int] = Field(default=0, ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    sku: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = None
    description: Optional[str] = None
    unit_price: Optional[Decimal] = Field(None, ge=0)
    stock_level: Optional[int] = Field(None, ge=0)

class ProductResponse(ProductBase):
    product_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ── Purchase Order Item Schemas ───────────────────────────

class POItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., ge=0)

class POItemCreate(POItemBase):
    pass

class POItemResponse(POItemBase):
    item_id: int
    line_total: Optional[Decimal] = None
    product: Optional[ProductResponse] = None

    class Config:
        from_attributes = True


# ── Purchase Order Schemas ────────────────────────────────

class PurchaseOrderCreate(BaseModel):
    vendor_id: int
    notes: Optional[str] = None
    items: List[POItemCreate] = Field(..., min_length=1)

class PurchaseOrderUpdate(BaseModel):
    status: str = Field(..., pattern="^(Pending|Approved|Rejected|Completed|Cancelled)$")

class PurchaseOrderResponse(BaseModel):
    po_id: int
    reference_no: str
    vendor_id: int
    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    status: str
    notes: Optional[str]
    created_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    vendor: Optional[VendorResponse] = None
    items: Optional[List[POItemResponse]] = []

    class Config:
        from_attributes = True


class PurchaseOrderListResponse(BaseModel):
    po_id: int
    reference_no: str
    vendor_id: int
    total_amount: Decimal
    status: str
    created_at: datetime
    vendor: Optional[VendorResponse] = None

    class Config:
        from_attributes = True


# ── User / Auth Schemas ──────────────────────────────────

class UserResponse(BaseModel):
    user_id: int
    email: str
    full_name: Optional[str]
    picture: Optional[str]
    provider: str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ── AI Schemas ───────────────────────────────────────────

class AIDescriptionRequest(BaseModel):
    product_name: str
    category: Optional[str] = "General"

class AIDescriptionResponse(BaseModel):
    product_name: str
    description: str


# ── Dashboard Schemas ────────────────────────────────────

class DashboardStats(BaseModel):
    total_pos: int
    pending_pos: int
    approved_pos: int
    rejected_pos: int
    completed_pos: int
    total_vendors: int
    total_products: int
    total_value: Decimal
