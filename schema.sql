-- ============================================================
-- ERP Purchase Order Management System — Database Schema
-- PostgreSQL
-- ============================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- USERS TABLE (for authentication)
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    user_id       SERIAL PRIMARY KEY,
    email         VARCHAR(255) UNIQUE NOT NULL,
    full_name     VARCHAR(255),
    picture       TEXT,
    provider      VARCHAR(50) DEFAULT 'google',
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- ============================================================
-- VENDORS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS vendors (
    vendor_id     SERIAL PRIMARY KEY,
    name          VARCHAR(255) NOT NULL,
    contact       VARCHAR(255),
    email         VARCHAR(255),
    gst_number    VARCHAR(20),
    address       TEXT,
    rating        NUMERIC(2,1) DEFAULT 0.0 CHECK (rating >= 0 AND rating <= 5),
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_vendors_name ON vendors(name);
CREATE INDEX idx_vendors_rating ON vendors(rating);

-- ============================================================
-- PRODUCTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS products (
    product_id    SERIAL PRIMARY KEY,
    name          VARCHAR(255) NOT NULL,
    sku           VARCHAR(100) UNIQUE NOT NULL,
    category      VARCHAR(100),
    brand         VARCHAR(100),
    unit_type     VARCHAR(50),
    expiry_date   DATE,
    batch_number  VARCHAR(50),
    minimum_stock INTEGER DEFAULT 10 CHECK (minimum_stock >= 0),
    gst_rate      NUMERIC(5,2) DEFAULT 5.00 CHECK (gst_rate IN (5.00, 12.00, 18.00)),
    description   TEXT,
    unit_price    NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    stock_level   INTEGER DEFAULT 0 CHECK (stock_level >= 0),
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_category ON products(category);

-- ============================================================
-- PURCHASE ORDERS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS purchase_orders (
    po_id         SERIAL PRIMARY KEY,
    reference_no  VARCHAR(50) UNIQUE NOT NULL,
    vendor_id     INTEGER NOT NULL REFERENCES vendors(vendor_id) ON DELETE RESTRICT,
    subtotal      NUMERIC(14,2) DEFAULT 0.00,
    tax_amount    NUMERIC(14,2) DEFAULT 0.00,
    total_amount  NUMERIC(14,2) DEFAULT 0.00,
    status        VARCHAR(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Rejected', 'Completed', 'Cancelled', 'Received')),
    stock_updated BOOLEAN DEFAULT FALSE,
    notes         TEXT,
    created_by    INTEGER REFERENCES users(user_id),
    created_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_po_reference ON purchase_orders(reference_no);
CREATE INDEX idx_po_vendor ON purchase_orders(vendor_id);
CREATE INDEX idx_po_status ON purchase_orders(status);
CREATE INDEX idx_po_created ON purchase_orders(created_at DESC);

-- ============================================================
-- PURCHASE ORDER ITEMS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS purchase_order_items (
    item_id       SERIAL PRIMARY KEY,
    po_id         INTEGER NOT NULL REFERENCES purchase_orders(po_id) ON DELETE CASCADE,
    product_id    INTEGER NOT NULL REFERENCES products(product_id) ON DELETE RESTRICT,
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    unit_price    NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    gst_rate      NUMERIC(5,2) DEFAULT 5.00 CHECK (gst_rate IN (5.00, 12.00, 18.00)),
    tax_amount    NUMERIC(14,2) DEFAULT 0.00 CHECK (tax_amount >= 0),
    line_total    NUMERIC(14,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    created_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_poi_po ON purchase_order_items(po_id);
CREATE INDEX idx_poi_product ON purchase_order_items(product_id);

-- ============================================================
-- EXTENSION MIGRATION BLOCK (safe for existing deployments)
-- ============================================================
ALTER TABLE vendors
    ADD COLUMN IF NOT EXISTS gst_number VARCHAR(20);

ALTER TABLE products
    ADD COLUMN IF NOT EXISTS brand VARCHAR(100),
    ADD COLUMN IF NOT EXISTS unit_type VARCHAR(50),
    ADD COLUMN IF NOT EXISTS expiry_date DATE,
    ADD COLUMN IF NOT EXISTS batch_number VARCHAR(50),
    ADD COLUMN IF NOT EXISTS minimum_stock INTEGER DEFAULT 10,
    ADD COLUMN IF NOT EXISTS gst_rate NUMERIC(5,2) DEFAULT 5.00;

ALTER TABLE purchase_orders
    ADD COLUMN IF NOT EXISTS stock_updated BOOLEAN DEFAULT FALSE;

ALTER TABLE purchase_order_items
    ADD COLUMN IF NOT EXISTS gst_rate NUMERIC(5,2) DEFAULT 5.00,
    ADD COLUMN IF NOT EXISTS tax_amount NUMERIC(14,2) DEFAULT 0.00;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'chk_po_status'
    ) THEN
        ALTER TABLE purchase_orders DROP CONSTRAINT chk_po_status;
    END IF;
    ALTER TABLE purchase_orders ADD CONSTRAINT chk_po_status
        CHECK (status IN ('Pending', 'Approved', 'Rejected', 'Completed', 'Cancelled', 'Received'));

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'chk_product_minimum_stock'
    ) THEN
        ALTER TABLE products ADD CONSTRAINT chk_product_minimum_stock CHECK (minimum_stock >= 0);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'chk_product_gst_rate'
    ) THEN
        ALTER TABLE products ADD CONSTRAINT chk_product_gst_rate CHECK (gst_rate IN (5.00, 12.00, 18.00));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'chk_item_gst_rate'
    ) THEN
        ALTER TABLE purchase_order_items ADD CONSTRAINT chk_item_gst_rate CHECK (gst_rate IN (5.00, 12.00, 18.00));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'chk_item_tax_amount'
    ) THEN
        ALTER TABLE purchase_order_items ADD CONSTRAINT chk_item_tax_amount CHECK (tax_amount >= 0);
    END IF;
END $$;
