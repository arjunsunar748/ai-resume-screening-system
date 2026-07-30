from typing import Generator
from app.db.session import SessionLocal


def get_db() -> Generator:
    """
    Dependency that yields a database session for a single HTTP request,
    ensuring cleanup and closure after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()