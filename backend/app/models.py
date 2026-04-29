import enum
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    staff = "staff"


class VendorStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    blacklisted = "blacklisted"


class BatchStatus(str, enum.Enum):
    active = "active"
    depleted = "depleted"
    expired = "expired"
    recalled = "recalled"


class POStatus(str, enum.Enum):
    draft = "draft"
    pending_approval = "pending_approval"
    approved = "approved"
    sent = "sent"
    partially_received = "partially_received"
    received = "received"
    cancelled = "cancelled"


class AlertType(str, enum.Enum):
    low_stock = "low_stock"
    expiry_warning = "expiry_warning"
    expiry_critical = "expiry_critical"
    expired = "expired"
    overstock = "overstock"
    po_overdue = "po_overdue"


class MovementType(str, enum.Enum):
    receipt = "receipt"
    sale = "sale"
    adjustment = "adjustment"
    return_ = "return"
    write_off = "write_off"
    transfer = "transfer"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.staff)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    oauth_provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    oauth_subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    contact_person: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str | None] = mapped_column(String(80), nullable=True)
    tax_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    payment_terms: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[VendorStatus] = mapped_column(Enum(VendorStatus), default=VendorStatus.active)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sku: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    barcode: Mapped[str | None] = mapped_column(String(100), nullable=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    category: Mapped[str | None] = mapped_column(String(120), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(40), nullable=True)
    unit_weight: Mapped[float | None] = mapped_column(Numeric(10, 3), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_perishable: Mapped[bool] = mapped_column(Boolean, default=False)
    shelf_life_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Stock(Base):
    __tablename__ = "stock"
    __table_args__ = (UniqueConstraint("product_id", "warehouse_location", name="uq_stock_product_location"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), index=True)
    warehouse_location: Mapped[str] = mapped_column(String(100), default="MAIN")
    current_qty: Mapped[float] = mapped_column(Numeric(12, 3), default=0)
    reserved_qty: Mapped[float] = mapped_column(Numeric(12, 3), default=0)
    reorder_level: Mapped[float] = mapped_column(Numeric(12, 3), default=0)
    reorder_qty: Mapped[float] = mapped_column(Numeric(12, 3), default=0)
    max_stock_level: Mapped[float | None] = mapped_column(Numeric(12, 3), nullable=True)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product: Mapped[Product] = relationship(Product)


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    po_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    vendor_id: Mapped[int | None] = mapped_column(ForeignKey("vendors.id"), nullable=True)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    approved_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    status: Mapped[POStatus] = mapped_column(Enum(POStatus), default=POStatus.draft)
    order_date: Mapped[date] = mapped_column(Date, default=date.today)
    expected_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    received_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    subtotal: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    tax_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    discount_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    total_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    shipping_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class POItem(Base):
    __tablename__ = "po_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    po_id: Mapped[int] = mapped_column(ForeignKey("purchase_orders.id", ondelete="CASCADE"), index=True)
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"), nullable=True)
    vendor_sku: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(String(300), nullable=True)
    ordered_qty: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)
    received_qty: Mapped[float] = mapped_column(Numeric(12, 3), default=0)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    tax_rate: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    discount_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    line_total: Mapped[float | None] = mapped_column(Numeric(14, 2), nullable=True)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class StockBatch(Base):
    __tablename__ = "stock_batches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    batch_number: Mapped[str] = mapped_column(String(100), nullable=False)
    received_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    quantity: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)
    remaining_qty: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)
    cost_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    po_id: Mapped[int | None] = mapped_column(ForeignKey("purchase_orders.id"), nullable=True)
    status: Mapped[BatchStatus] = mapped_column(Enum(BatchStatus), default=BatchStatus.active)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[AlertType] = mapped_column(Enum(AlertType), nullable=False)
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"), nullable=True)
    batch_id: Mapped[int | None] = mapped_column(ForeignKey("stock_batches.id"), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"), nullable=True)
    batch_id: Mapped[int | None] = mapped_column(ForeignKey("stock_batches.id"), nullable=True)
    movement_type: Mapped[MovementType] = mapped_column(Enum(MovementType), nullable=False)
    quantity: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)
    reference_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reference_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
