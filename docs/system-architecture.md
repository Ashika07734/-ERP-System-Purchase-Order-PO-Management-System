# GroceryERP System Architecture Overview

## 1) System Architecture

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        GROCERY ERP SYSTEM                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐    │
│   │  Frontend   │    │   Backend   │    │      Database       │    │
│   │ HTML+CSS+JS │◄──►│ FastAPI     │◄──►│ PostgreSQL + Redis  │    │
│   │ (Nginx)     │    │ (Python)    │    │ (optional cache)    │    │
│   └─────────────┘    └─────────────┘    └─────────────────────┘    │
│          │                  │                      │                │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐    │
│   │  PDF Engine │    │  Auth/RBAC  │    │   File Storage      │    │
│   │ Puppeteer   │    │ JWT/OAuth   │    │ AWS S3 / Local      │    │
│   └─────────────┘    └─────────────┘    └─────────────────────┘    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 2) Design Decision Log

- Batch tracking: FIFO stock depletion with separate stock_batches table.
- Expiry alerts: 30d warning, 7d critical, 0d expired; configurable by admin.
- Print/PDF: print CSS for client-side print and Puppeteer endpoint for server-side PDF.
- PO workflow: draft -> approval -> sent -> receipt with role checks.
- Auto reorder: optional auto-draft PO when stock is critically low.
- Audit trail: all stock mutations recorded in stock_movements.
- Multi-warehouse: stock uniqueness by product_id and warehouse_location.
- Search: designed for PostgreSQL full-text search with GIN indexes.

## 3) Background Jobs

Nightly 00:01:
- evaluate stock_batches expiry windows
- upsert expiry alerts (warning/critical/expired)
- mark expired batches

Hourly:
- evaluate low-stock state against reorder thresholds
- upsert low_stock alerts where active alert does not exist

PO receipt event:
- increase stock.current_qty
- insert stock_batch records
- insert stock_movement rows
- update po_items.received_qty

Delivery channels:
- in-app notifications via WebSocket/SSE
- optional daily email digest
- optional SMS for critical alerts
