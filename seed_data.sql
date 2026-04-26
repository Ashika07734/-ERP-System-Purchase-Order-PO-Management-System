-- ============================================================
-- ERP Purchase Order Management System — Seed Data
-- ============================================================

-- Sample Users
INSERT INTO users (email, full_name, picture, provider) VALUES
('admin@erpcloud.io', 'Admin User', NULL, 'local'),
('john.doe@example.com', 'John Doe', NULL, 'google'),
('jane.smith@example.com', 'Jane Smith', NULL, 'google');

-- Sample Vendors
INSERT INTO vendors (name, contact, email, gst_number, address, rating) VALUES
('FreshMart Distributors',      '+1-555-1101', 'sales@freshmartdist.com',  '27AAACF1234B1ZK', '100 Market Yard, Chicago, IL 60601',   4.6),
('GoldenGrain Wholesale',       '+1-555-1102', 'orders@goldengrain.com',   '27AAAGG5678K1Z3', '250 Food Hub Ave, San Jose, CA 95110',  4.7),
('DailyDairy Supply Co.',       '+1-555-1103', 'info@dailydairy.com',      '27AAADD9012P1ZX', '78 Cold Chain Road, Detroit, MI 48201',  4.4),
('SpiceRoute Traders',          '+1-555-1104', 'supply@spiceroute.com',    '27AAASR4567Q1Z8', '500 Wholesale Street, Houston, TX 77001', 4.3),
('QuickSnack FMCG',             '+1-555-1105', 'sales@quicksnackfmcg.com', '27AAAQS8934R1Z2', '12 Distribution Park, New York, NY 10001', 4.5),
('PureDrop Beverages',          '+1-555-1106', 'ptl@puredropbev.com',      '27AAAPD7788M1ZT', '300 Harbor Commerce, Long Beach, CA 90802', 4.2),
('CleanNest Essentials',        '+1-555-1107', 'eu@cleannest.co.uk',       '27AAACN3344N1ZL', '45 Retail Avenue, London, UK EC2A 1AF', 4.1),
('FrozenCart Foods',            '+1-555-1108', 'orders@frozencart.com',    '27AAAFC8899T1ZA', '88 Warehouse Lane, Memphis, TN 38103', 4.0);

-- Sample Products
INSERT INTO products (name, sku, category, brand, unit_type, expiry_date, batch_number, minimum_stock, gst_rate, description, unit_price, stock_level) VALUES
('Basmati Rice 25kg',               'RICE-BSM-001',  'Rice',              'Royal Harvest',  'Bag',    '2027-03-31', 'BR-2503-A1',  50,  5.00,  'Premium long-grain basmati rice for wholesale supply.',                42.50,  220),
('Whole Wheat Flour 10kg',          'FLR-WHT-002',   'Flour',             'Aashirvaad',     'Bag',    '2026-12-15', 'WF-2612-B2',  40,  5.00,  'Stone-milled atta flour suitable for retail repackaging.',             19.75,  180),
('Refined Sunflower Oil 1L',        'OIL-SFL-003',   'Oil',               'Fortune',        'Bottle', '2027-01-20', 'SO-2701-C3', 120,  5.00,  'Refined sunflower oil in 1 liter bottles.',                             2.10,  520),
('Potato Chips Classic 52g',        'SNK-CHP-004',   'Snacks',            'Layz',           'Packet', '2026-09-10', 'PC-2609-D1', 200, 12.00,  'Classic salted potato chips, FMCG fast-moving snack item.',             0.55,  900),
('Mango Juice 1L',                  'BEV-MNG-005',   'Beverages',         'Tropico',        'Bottle', '2026-11-25', 'MJ-2611-E4', 150, 12.00,  'Ready-to-serve mango juice with fruit pulp.',                           1.45,  420),
('UHT Milk 1L',                     'DRY-MLK-006',   'Dairy',             'AmulFresh',      'Packet', '2026-08-01', 'ML-2608-F2', 180,  5.00,  'Long shelf-life UHT milk for supermarket channels.',                    1.20,  300),
('Turmeric Powder 500g',            'SPC-TRM-007',   'Spices',            'EverSpice',      'Packet', '2027-06-30', 'TP-2706-G5', 100,  5.00,  'Ground turmeric powder in moisture-proof laminated packs.',             1.10,  260),
('Frozen Green Peas 500g',          'FRZ-PEA-008',   'Frozen Foods',      'IceField',       'Packet', '2026-10-05', 'FG-2610-H3', 140,  5.00,  'IQF frozen peas for horeca and retail distribution.',                   1.35,  110),
('Dishwash Liquid 500ml',           'CLN-DWL-009',   'Cleaning Products', 'SparkleHome',    'Bottle', '2027-02-14', 'DL-2702-J9',  90, 18.00,  'Lemon dishwashing liquid for kitchen cleaning.',                        1.90,   85),
('Gram Flour 1kg',                  'FLR-GRM-010',   'Flour',             'GoodGrain',      'Packet', '2027-01-31', 'GF-2701-K7', 110,  5.00,  'Fine gram flour suitable for snacks and household use.',                1.05,  240),
('Chocolate Wafer Box (24 pcs)',    'SNK-WFR-011',   'Snacks',            'CrunchBite',     'Box',    '2026-12-28', 'CW-2612-L4',  80, 12.00,  'Assorted chocolate wafer bars in trade pack.',                          6.80,   75),
('Detergent Powder 1kg',            'CLN-DTR-012',   'Cleaning Products', 'BrightWash',     'Packet', '2027-04-12', 'DP-2704-M6', 130, 18.00,  'High-foam detergent powder for household laundry.',                     2.35,   65);

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
