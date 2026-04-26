"""
ERP PO Management System — SQLAlchemy ORM Models
"""

from sqlalchemy import (
    Column, Integer, String, Numeric, Boolean, Text,
    ForeignKey, DateTime, CheckConstraint, Date
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


class User(Base):
    __tablename__ = "users"

    user_id    = Column(Integer, primary_key=True, index=True)
    email      = Column(String(255), unique=True, nullable=False, index=True)
    full_name  = Column(String(255))
    picture    = Column(Text)
    provider   = Column(String(50), default="google")
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    purchase_orders = relationship("PurchaseOrder", back_populates="creator")


class Vendor(Base):
    __tablename__ = "vendors"

    vendor_id  = Column(Integer, primary_key=True, index=True)
    name       = Column(String(255), nullable=False)
    contact    = Column(String(255))
    email      = Column(String(255))
    gst_number = Column(String(20))
    address    = Column(Text)
    rating     = Column(Numeric(2, 1), default=0.0)
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("rating >= 0 AND rating <= 5", name="chk_vendor_rating"),
    )

    # Relationships
    purchase_orders = relationship("PurchaseOrder", back_populates="vendor")


class Product(Base):
    __tablename__ = "products"

    product_id  = Column(Integer, primary_key=True, index=True)
    name        = Column(String(255), nullable=False)
    sku         = Column(String(100), unique=True, nullable=False, index=True)
    category    = Column(String(100))
    brand       = Column(String(100))
    unit_type   = Column(String(50))
    expiry_date = Column(Date)
    batch_number = Column(String(50))
    minimum_stock = Column(Integer, default=10)
    gst_rate    = Column(Numeric(5, 2), default=5.00)
    description = Column(Text)
    unit_price  = Column(Numeric(12, 2), nullable=False)
    stock_level = Column(Integer, default=0)
    is_active   = Column(Boolean, default=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("unit_price >= 0", name="chk_product_price"),
        CheckConstraint("stock_level >= 0", name="chk_product_stock"),
        CheckConstraint("minimum_stock >= 0", name="chk_product_minimum_stock"),
        CheckConstraint("gst_rate IN (5.00, 12.00, 18.00)", name="chk_product_gst_rate"),
    )

    # Relationships
    order_items = relationship("PurchaseOrderItem", back_populates="product")


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    po_id        = Column(Integer, primary_key=True, index=True)
    reference_no = Column(String(50), unique=True, nullable=False, index=True)
    vendor_id    = Column(Integer, ForeignKey("vendors.vendor_id", ondelete="RESTRICT"), nullable=False)
    subtotal     = Column(Numeric(14, 2), default=0.00)
    tax_amount   = Column(Numeric(14, 2), default=0.00)
    total_amount = Column(Numeric(14, 2), default=0.00)
    status       = Column(String(20), default="Pending")
    stock_updated = Column(Boolean, default=False)
    notes        = Column(Text)
    created_by   = Column(Integer, ForeignKey("users.user_id"))
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint(
            "status IN ('Pending', 'Approved', 'Rejected', 'Completed', 'Cancelled', 'Received')",
            name="chk_po_status"
        ),
    )

    # Relationships
    vendor  = relationship("Vendor", back_populates="purchase_orders")
    creator = relationship("User", back_populates="purchase_orders")
    items   = relationship("PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan")


class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"

    item_id    = Column(Integer, primary_key=True, index=True)
    po_id      = Column(Integer, ForeignKey("purchase_orders.po_id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="RESTRICT"), nullable=False)
    quantity   = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    gst_rate   = Column(Numeric(5, 2), default=5.00)
    tax_amount = Column(Numeric(14, 2), default=0.00)
    line_total = Column(Numeric(14, 2), default=0.00)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("quantity > 0", name="chk_item_qty"),
        CheckConstraint("unit_price >= 0", name="chk_item_price"),
        CheckConstraint("gst_rate IN (5.00, 12.00, 18.00)", name="chk_item_gst_rate"),
        CheckConstraint("tax_amount >= 0", name="chk_item_tax_amount"),
    )

    # Relationships
    purchase_order = relationship("PurchaseOrder", back_populates="items")
    product        = relationship("Product", back_populates="order_items")
