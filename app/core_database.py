# core_database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# Path to your SQLite database file
DATABASE_URL = "sqlite:///./data/productivity.db"

# Create the database engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for your models to inherit
Base = declarative_base()

# Dependency to get DB session
def get_user_log_for_date(user_id: int, target_date, db: Session):
    """
    Fetches the user's daily log for a specific date.
    """
    return db.query(DailyLog).filter(
        DailyLog.user_id == user_id,
        func.date(DailyLog.created_at) == target_date
    ).first()

# Function to create the database tables
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()