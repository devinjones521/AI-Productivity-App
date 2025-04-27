# models.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class DailyLog(Base):
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # 👈 Add this line
    user_log = Column(String, nullable=False)
    ai_summary = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
