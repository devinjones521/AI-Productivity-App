from sqlalchemy.orm import Session
from .openai_service import summarize_user_log
from ..models import DailyLog
from sqlalchemy import func



def generate_daily_summary(user_id: int, target_date, db):
    user_log_entry = get_user_log_for_date(user_id=user_id, target_date=target_date, db=db)

    if not user_log_entry:
        return "No daily log found for today."

    user_log_text = user_log_entry.user_log

    summary = summarize_user_log(user_log_text)
    return summary

# Dependency to get DB session
def get_user_log_for_date(user_id: int, target_date, db: Session):
    """
    Fetches the user's daily log for a specific date.
    """
    return db.query(DailyLog).filter(
        DailyLog.user_id == user_id,
        func.date(DailyLog.created_at) == target_date
    ).first()