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
    status        VARCHAR(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Rejected', 'Completed', 'Cancelled')),
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
    line_total    NUMERIC(14,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    created_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_poi_po ON purchase_order_items(po_id);
CREATE INDEX idx_poi_product ON purchase_order_items(product_id);
