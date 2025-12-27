from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Use SQLite for development (simple & interview-safe)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./medication_india.db"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Dependency for DB session (used later in APIs)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
