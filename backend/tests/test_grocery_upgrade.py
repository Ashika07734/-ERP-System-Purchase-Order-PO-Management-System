"""Integration tests for the grocery/FMCG upgrade."""

from __future__ import annotations

import os
from decimal import Decimal
from pathlib import Path
from typing import Any
import unittest
from types import SimpleNamespace

from fastapi.testclient import TestClient

TEST_DB_PATH = Path(__file__).resolve().parents[2] / "grocery_upgrade_test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH.as_posix()}"
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")
os.environ.setdefault("JWT_EXPIRY_MINUTES", "60")
os.environ.setdefault("GOOGLE_CLIENT_ID", "test-client-id")
os.environ.setdefault("GOOGLE_CLIENT_SECRET", "test-client-secret")

from backend.auth import get_current_user, get_or_create_user
from backend.database import Base, SessionLocal, engine
from backend.main import app
from backend.models import PurchaseOrder, PurchaseOrderItem, Product, User, Vendor


class GroceryUpgradeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if TEST_DB_PATH.exists():
            TEST_DB_PATH.unlink()

        Base.metadata.create_all(bind=engine)

        cls.client_context = TestClient(app)
        cls.client = cls.client_context.__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            cls.client_context.__exit__(None, None, None)
        finally:
            app.dependency_overrides.clear()
            engine.dispose()
            if TEST_DB_PATH.exists():
                TEST_DB_PATH.unlink()

    def setUp(self) -> None:
        self._clear_tables()
        with SessionLocal() as db:
            current_user = get_or_create_user(
                db,
                email="tester@erpcloud.io",
                full_name="Test User",
            )
            db.commit()
            self.current_user_id = current_user.user_id
            self.current_user_email = current_user.email

        # Keep auth dependency independent from SQLAlchemy session lifecycle.
        app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
            user_id=self.current_user_id,
            email=self.current_user_email,
        )

    def tearDown(self) -> None:
        app.dependency_overrides.clear()

    def _clear_tables(self) -> None:
        with SessionLocal() as db:
            db.query(PurchaseOrderItem).delete()
            db.query(PurchaseOrder).delete()
            db.query(Product).delete()
            db.query(Vendor).delete()
            db.query(User).delete()
            db.commit()

    def _create_vendor(self, name: str = "FreshMart Distributors") -> int:
        response = self.client.post(
            "/api/vendors",
            json={
                "name": name,
                "contact": "+1-555-1101",
                "email": "sales@example.com",
                "gst_number": "27AAACF1234B1ZK",
                "address": "100 Market Yard, Chicago, IL 60601",
                "rating": 4.6,
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()["vendor_id"]

    def _create_product(self, overrides: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = {
            "name": "Basmati Rice 25kg",
            "sku": f"RICE-{os.urandom(3).hex().upper()}",
            "category": "Rice",
            "brand": "Royal Harvest",
            "unit_type": "Bag",
            "expiry_date": "2027-03-31",
            "batch_number": "BR-2503-A1",
            "minimum_stock": 20,
            "gst_rate": 5,
            "description": "Premium long-grain basmati rice.",
            "unit_price": 42.5,
            "stock_level": 5,
        }
        if overrides:
            payload.update(overrides)

        response = self.client.post("/api/products", json=payload)
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()

    def test_purchase_order_applies_gst_and_updates_stock(self) -> None:
        vendor_id = self._create_vendor()
        product = self._create_product({"stock_level": 5, "minimum_stock": 20})

        response = self.client.post(
            "/api/purchase-orders",
            json={
                "vendor_id": vendor_id,
                "notes": "Rice restock",
                "items": [
                    {
                        "product_id": product["product_id"],
                        "quantity": 4,
                        "unit_price": 100,
                        "gst_rate": 12,
                    }
                ],
            },
        )

        self.assertEqual(response.status_code, 201, response.text)
        body = response.json()

        self.assertEqual(Decimal(str(body["subtotal"])), Decimal("400.00"))
        self.assertEqual(Decimal(str(body["tax_amount"])), Decimal("48.00"))
        self.assertEqual(Decimal(str(body["total_amount"])), Decimal("448.00"))
        self.assertTrue(body["stock_updated"])
        self.assertTrue(any("Low Stock Alert" in alert for alert in body.get("low_stock_alerts", [])))

        product_response = self.client.get(f"/api/products/{product['product_id']}")
        self.assertEqual(product_response.status_code, 200, product_response.text)
        self.assertEqual(product_response.json()["stock_level"], 9)

    def test_dashboard_includes_low_stock_products(self) -> None:
        vendor_id = self._create_vendor("QuickSnack FMCG")
        product = self._create_product({"stock_level": 2, "minimum_stock": 15, "brand": "CrunchBite"})

        response = self.client.post(
            "/api/purchase-orders",
            json={
                "vendor_id": vendor_id,
                "notes": "Snack restock",
                "items": [
                    {
                        "product_id": product["product_id"],
                        "quantity": 1,
                        "unit_price": 10,
                        "gst_rate": 18,
                    }
                ],
            },
        )
        self.assertEqual(response.status_code, 201, response.text)

        stats_response = self.client.get("/api/purchase-orders/stats")
        self.assertEqual(stats_response.status_code, 200, stats_response.text)
        stats = stats_response.json()

        low_stock_names = [item["name"] for item in stats.get("low_stock_products", [])]
        self.assertIn(product["name"], low_stock_names)

    def test_received_status_updates_legacy_purchase_order_stock(self) -> None:
        vendor_id = self._create_vendor("Legacy Vendor")
        product = self._create_product({"stock_level": 0, "minimum_stock": 10})

        with SessionLocal() as db:
            po = PurchaseOrder(
                reference_no="PO-LEGACY-00001",
                vendor_id=vendor_id,
                subtotal=Decimal("120.00"),
                tax_amount=Decimal("6.00"),
                total_amount=Decimal("126.00"),
                status="Pending",
                stock_updated=False,
                notes="Legacy inbound shipment",
                created_by=self.current_user_id,
            )
            db.add(po)
            db.flush()
            db.add(
                PurchaseOrderItem(
                    po_id=po.po_id,
                    product_id=product["product_id"],
                    quantity=12,
                    unit_price=Decimal("10.00"),
                    gst_rate=Decimal("5.00"),
                    tax_amount=Decimal("6.00"),
                    line_total=Decimal("120.00"),
                )
            )
            db.commit()
            legacy_po_id = po.po_id

        response = self.client.put(
            f"/api/purchase-orders/{legacy_po_id}/status",
            json={"status": "Received"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertEqual(body["status"], "Received")
        self.assertTrue(body["stock_updated"])

        product_response = self.client.get(f"/api/products/{product['product_id']}")
        self.assertEqual(product_response.status_code, 200, product_response.text)
        self.assertEqual(product_response.json()["stock_level"], 12)


if __name__ == "__main__":
    unittest.main()
