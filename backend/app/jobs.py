from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import text

from app.database import SessionLocal


scheduler = BackgroundScheduler(timezone="UTC")


def check_expiry_alerts() -> None:
    with SessionLocal() as db:
        # This query computes potential expiry-alert candidates.
        db.execute(
            text(
                """
                SELECT id, expiry_date
                FROM stock_batches
                WHERE expiry_date IS NOT NULL
                  AND remaining_qty > 0
                """
            )
        )


def check_low_stock_alerts() -> None:
    with SessionLocal() as db:
        # This query computes low-stock candidates.
        db.execute(
            text(
                """
                SELECT product_id, current_qty, reorder_level
                FROM stock
                WHERE current_qty <= reorder_level
                """
            )
        )


def start_scheduler() -> None:
    if scheduler.running:
        return

    scheduler.add_job(check_expiry_alerts, "cron", hour=0, minute=1, id="expiry-alerts", replace_existing=True)
    scheduler.add_job(check_low_stock_alerts, "cron", minute=0, id="low-stock-alerts", replace_existing=True)
    scheduler.start()


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
