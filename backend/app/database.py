from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine_kwargs = {"pool_pre_ping": True}
if settings.database_url.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}


def _sqlite_fallback_url() -> str:
    db_path = Path(__file__).resolve().parents[2] / "groceryerp.db"
    return f"sqlite:///{db_path.as_posix()}"


def _build_engine(database_url: str):
    kwargs = dict(engine_kwargs)
    if database_url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
    return create_engine(database_url, **kwargs)


engine = _build_engine(settings.database_url)

try:
    with engine.connect():
        pass
except SQLAlchemyError as exc:
    if not settings.database_url.startswith("sqlite"):
        print(f"[WARNING] PostgreSQL unavailable, falling back to SQLite: {exc}")
        engine = _build_engine(_sqlite_fallback_url())
    else:
        raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
