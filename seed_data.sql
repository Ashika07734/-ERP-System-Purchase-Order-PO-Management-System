-- ============================================================
-- ERP Purchase Order Management System — Seed Data
-- ============================================================

-- Sample Users
INSERT INTO users (email, full_name, picture, provider) VALUES
('admin@erpcloud.io', 'Admin User', NULL, 'local'),
('john.doe@example.com', 'John Doe', NULL, 'google'),
('jane.smith@example.com', 'Jane Smith', NULL, 'google');

-- Sample Vendors
INSERT INTO vendors (name, contact, email, address, rating) VALUES
('Acme Industrial Supplies',   '+1-555-0101', 'sales@acme-ind.com',     '100 Industrial Blvd, Chicago, IL 60601',       4.5),
('GlobalTech Components',      '+1-555-0202', 'orders@globaltech.com',  '250 Innovation Dr, San Jose, CA 95110',        4.8),
('PrimeParts Manufacturing',   '+1-555-0303', 'info@primeparts.com',    '78 Factory Lane, Detroit, MI 48201',           4.2),
('Vertex Raw Materials',       '+1-555-0404', 'supply@vertex-rm.com',   '500 Commerce St, Houston, TX 77001',           3.9),
('NexGen Office Solutions',    '+1-555-0505', 'sales@nexgenoffice.com', '12 Business Park Ave, New York, NY 10001',     4.6),
('Pacific Trade Logistics',    '+1-555-0606', 'ptl@pacifictrade.com',   '300 Harbor Way, Long Beach, CA 90802',         4.1),
('EuroParts International',    '+44-20-7946',  'eu@europarts.co.uk',    '45 King Road, London, UK EC2A 1AF',            4.7),
('SilverLine Packaging',       '+1-555-0808', 'orders@silverline.com',  '88 Pack St, Memphis, TN 38103',                3.8);

-- Sample Products
INSERT INTO products (name, sku, category, description, unit_price, stock_level) VALUES
('Stainless Steel Bolt M10',       'SSB-M10-001',   'Hardware',      'High-grade stainless steel hex bolt, M10x50mm',           2.50,   5000),
('Industrial Bearing 6205',        'BRG-6205-002',  'Bearings',      'Deep groove ball bearing, 25x52x15mm',                    12.75,  1200),
('Hydraulic Hose 1/2" x 3m',       'HYD-H12-003',  'Hydraulics',    'Reinforced hydraulic hose, 1/2 inch, 3 meter length',     34.00,   800),
('LED Panel Light 60W',            'LED-PNL-004',   'Electrical',    '600x600mm recessed LED panel, 6500K daylight',            45.99,   350),
('Copper Wire 2.5mm² (100m)',      'COP-W25-005',   'Electrical',    'Single core copper cable, 100 meter roll',                78.50,   200),
('Safety Helmet – Class E',        'SAF-HLM-006',   'Safety',        'ANSI Z89.1 certified hard hat, adjustable ratchet',       18.25,  1500),
('Welding Rod E7018 (5kg)',        'WLD-718-007',   'Welding',       'Low hydrogen electrode, 3.2mm, 5kg pack',                 22.00,   900),
('Pneumatic Cylinder 50x200',      'PNU-C50-008',   'Pneumatics',    'Double-acting pneumatic cylinder, 50mm bore, 200mm stroke', 89.00,  150),
('Industrial Lubricant 5L',        'LUB-IND-009',   'Chemicals',     'Multi-purpose industrial lubricant, 5 liter can',         32.50,   400),
('Thermal Printer Paper (50 rolls)','TPP-50R-010',  'Office',        'BPA-free thermal receipt paper, 80x80mm, box of 50',      28.00,   600),
('Carbon Steel Pipe DN50',        'CSP-DN50-011',  'Piping',        'Schedule 40 carbon steel pipe, 2 inch, 6m length',        125.00,   100),
('Nitrile Gloves Box (Large)',     'GLV-NIT-012',   'Safety',        'Powder-free nitrile gloves, large, box of 100',            9.99,  3000);

-- Sample Purchase Orders
INSERT INTO purchase_orders (reference_no, vendor_id, subtotal, tax_amount, total_amount, status, notes, created_by) VALUES
('PO-2026-00001', 1, 1250.00, 62.50, 1312.50, 'Approved',  'Monthly hardware restock',          1),
('PO-2026-00002', 2, 3450.00, 172.50, 3622.50, 'Pending',   'Q2 bearing and component order',    1),
('PO-2026-00003', 3, 890.00,  44.50,  934.50,  'Completed', 'Urgent welding supplies',           2),
('PO-2026-00004', 5, 567.00,  28.35,  595.35,  'Pending',   'Office supplies reorder',           2),
('PO-2026-00005', 4, 2100.00, 105.00, 2205.00, 'Rejected',  'Budget exceeded — needs revision',  1),
('PO-2026-00006', 6, 4500.00, 225.00, 4725.00, 'Approved',  'Annual logistics contract order',   3),
('PO-2026-00007', 7, 1875.00, 93.75,  1968.75, 'Pending',   'European parts import',             1);

-- Sample Purchase Order Items
INSERT INTO purchase_order_items (po_id, product_id, quantity, unit_price) VALUES
-- PO-2026-00001
(1, 1,  200, 2.50),
(1, 6,  40,  18.25),
-- PO-2026-00002
(2, 2,  100, 12.75),
(2, 8,  20,  89.00),
(2, 3,  15,  34.00),
-- PO-2026-00003
(3, 7,  30,  22.00),
(3, 9,  4,   32.50),
-- PO-2026-00004
(4, 10, 15,  28.00),
(4, 12, 15,  9.99),
-- PO-2026-00005
(5, 11, 12,  125.00),
(5, 5,  6,   78.50),
-- PO-2026-00006
(6, 3,  50,  34.00),
(6, 8,  25,  89.00),
(6, 9,  10,  32.50),
-- PO-2026-00007
(7, 2,  50,  12.75),
(7, 4,  20,  45.99),
(7, 1,  100, 2.50);
