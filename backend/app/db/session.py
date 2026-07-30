from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# Initialize SQLAlchemy Engine
# pool_pre_ping=True checks connection health before issuing queries to prevent stale connection errors
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Create a scoped SessionLocal class for handling request-bound DB transactions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Declarative Base Class for all SQLAlchemy ORM models
class Base(DeclarativeBase):
    pass