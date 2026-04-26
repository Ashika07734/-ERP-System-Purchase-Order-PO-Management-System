"""Seed the ERP database with sample data via API."""
import httpx

BASE = "http://localhost:8000"

# Get token
r = httpx.post(f"{BASE}/auth/dev-login")
token = r.json()["access_token"]
h = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Create vendors
vendors = [
    {"name": "Acme Industrial Supplies", "contact": "+1-555-0101", "email": "sales@acme-ind.com", "rating": 4.5},
    {"name": "GlobalTech Components", "contact": "+1-555-0202", "email": "orders@globaltech.com", "rating": 4.8},
    {"name": "PrimeParts Manufacturing", "contact": "+1-555-0303", "email": "info@primeparts.com", "rating": 4.2},
    {"name": "NexGen Office Solutions", "contact": "+1-555-0505", "email": "sales@nexgenoffice.com", "rating": 4.6},
]
for v in vendors:
    r = httpx.post(f"{BASE}/api/vendors", headers=h, json=v)
    print(f"  Vendor {v['name']}: {r.status_code}")

# Create products
products = [
    {"name": "Stainless Steel Bolt M10", "sku": "SSB-M10-001", "category": "Hardware", "unit_price": 2.50, "stock_level": 5000},
    {"name": "Industrial Bearing 6205", "sku": "BRG-6205-002", "category": "Bearings", "unit_price": 12.75, "stock_level": 1200},
    {"name": "LED Panel Light 60W", "sku": "LED-PNL-004", "category": "Electrical", "unit_price": 45.99, "stock_level": 350},
    {"name": "Safety Helmet Class E", "sku": "SAF-HLM-006", "category": "Safety", "unit_price": 18.25, "stock_level": 1500},
    {"name": "Welding Rod E7018", "sku": "WLD-718-007", "category": "Welding", "unit_price": 22.00, "stock_level": 900},
    {"name": "Industrial Lubricant 5L", "sku": "LUB-IND-009", "category": "Chemicals", "unit_price": 32.50, "stock_level": 400},
]
for p in products:
    r = httpx.post(f"{BASE}/api/products", headers=h, json=p)
    print(f"  Product {p['name']}: {r.status_code}")

# Create POs
pos = [
    {"vendor_id": 1, "notes": "Monthly hardware restock", "items": [
        {"product_id": 1, "quantity": 200, "unit_price": 2.50},
        {"product_id": 4, "quantity": 40, "unit_price": 18.25},
    ]},
    {"vendor_id": 2, "notes": "Q2 bearing order", "items": [
        {"product_id": 2, "quantity": 100, "unit_price": 12.75},
        {"product_id": 3, "quantity": 20, "unit_price": 45.99},
    ]},
    {"vendor_id": 3, "notes": "Urgent welding supplies", "items": [
        {"product_id": 5, "quantity": 30, "unit_price": 22.00},
        {"product_id": 6, "quantity": 4, "unit_price": 32.50},
    ]},
    {"vendor_id": 4, "notes": "Office safety equipment", "items": [
        {"product_id": 4, "quantity": 60, "unit_price": 18.25},
        {"product_id": 6, "quantity": 10, "unit_price": 32.50},
    ]},
]
for i, po in enumerate(pos, 1):
    r = httpx.post(f"{BASE}/api/purchase-orders", headers=h, json=po)
    print(f"  PO {i}: {r.status_code}")

# Update statuses
httpx.put(f"{BASE}/api/purchase-orders/1/status", headers=h, json={"status": "Approved"})
httpx.put(f"{BASE}/api/purchase-orders/3/status", headers=h, json={"status": "Completed"})
httpx.put(f"{BASE}/api/purchase-orders/4/status", headers=h, json={"status": "Rejected"})
print("All statuses updated. Seeding complete!")
