# services/daily_log_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.daily_log import DailyLog
from app.services.openai_service import summarize_user_log

def get_user_log_for_date(user_id: int, target_date, db: Session):
    """
    Fetches the user's daily log for a specific date.
    """
    return db.query(DailyLog).filter(
        DailyLog.user_id == user_id,
        func.date(DailyLog.created_at) == target_date
    ).first()

def generate_daily_summary(user_id: int, target_date, db: Session):
    """
    Generates a daily AI summary based on the user's log for the day.
    """
    user_log_entry = get_user_log_for_date(user_id=user_id, target_date=target_date, db=db)

    if not user_log_entry:
        return "No daily log found for today."

    user_log_text = user_log_entry.user_log

    summary = summarize_user_log(user_log_text)
    return summary
