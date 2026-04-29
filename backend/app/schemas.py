from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field

from app.models import AlertType, POStatus, UserRole, VendorStatus


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=2)
    role: UserRole = UserRole.staff


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OAuthCodeRequest(BaseModel):
    code: str
    redirect_uri: str


class VendorBase(BaseModel):
    name: str
    contact_person: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    city: str | None = None
    tax_id: str | None = None
    payment_terms: str | None = None
    status: VendorStatus = VendorStatus.active
    notes: str | None = None


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: str | None = None
    contact_person: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    city: str | None = None
    tax_id: str | None = None
    payment_terms: str | None = None
    status: VendorStatus | None = None
    notes: str | None = None


class VendorRead(VendorBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ProductBase(BaseModel):
    name: str
    sku: str
    barcode: str | None = None
    category: str | None = None
    price: float = 0
    unit: str | None = None
    unit_weight: float | None = None
    description: str | None = None
    image_url: str | None = None
    is_perishable: bool = False
    shelf_life_days: int | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    barcode: str | None = None
    category: str | None = None
    price: float | None = None
    unit: str | None = None
    unit_weight: float | None = None
    description: str | None = None
    image_url: str | None = None
    is_perishable: bool | None = None
    shelf_life_days: int | None = None


class ProductRead(ProductBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class StockAdjustRequest(BaseModel):
    product_id: int
    warehouse_location: str = "MAIN"
    quantity_delta: float
    notes: str | None = None


class BatchCreateRequest(BaseModel):
    product_id: int
    batch_number: str
    received_date: date
    expiry_date: date | None = None
    quantity: float = Field(gt=0)
    cost_price: float | None = None
    warehouse_location: str = "MAIN"


class StockRead(BaseModel):
    id: int
    product_id: int
    warehouse_location: str
    current_qty: float
    reserved_qty: float
    reorder_level: float
    reorder_qty: float
    max_stock_level: float | None
    last_updated: datetime

    model_config = {"from_attributes": True}


class POItemIn(BaseModel):
    product_id: int
    ordered_qty: float = Field(gt=0)
    unit_price: float = Field(ge=0)
    tax_rate: float = Field(default=0, ge=0)
    discount_pct: float = Field(default=0, ge=0)
    vendor_sku: str | None = None
    description: str | None = None
    expiry_date: date | None = None
    notes: str | None = None


class POCreate(BaseModel):
    vendor_id: int
    expected_date: date | None = None
    notes: str | None = None
    shipping_address: str | None = None
    items: list[POItemIn]


class POUpdate(BaseModel):
    expected_date: date | None = None
    notes: str | None = None
    shipping_address: str | None = None


class POReceiveItem(BaseModel):
    po_item_id: int
    received_qty: float = Field(gt=0)
    batch_number: str
    expiry_date: date | None = None


class POReceiveRequest(BaseModel):
    items: list[POReceiveItem]
    received_date: date = Field(default_factory=date.today)


class PORead(BaseModel):
    id: int
    po_number: str
    vendor_id: int | None
    status: POStatus
    order_date: date
    expected_date: date | None
    received_date: date | None
    subtotal: float
    tax_amount: float
    discount_amount: float
    total_amount: float
    notes: str | None
    shipping_address: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AlertRead(BaseModel):
    id: int
    type: AlertType
    product_id: int | None
    batch_id: int | None
    message: str
    is_read: bool
    is_resolved: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AIChatRequest(BaseModel):
    prompt: str = Field(min_length=2)


class AIChatResponse(BaseModel):
    provider: str
    model: str
    response: str
