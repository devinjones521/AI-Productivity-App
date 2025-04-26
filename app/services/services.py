from ..core_database import get_user_log_for_date
from .openai_service import summarize_user_log

def generate_daily_summary(user_id: int, target_date, db):
    user_log_entry = get_user_log_for_date(user_id=user_id, target_date=target_date, db=db)

    if not user_log_entry:
        return "No daily log found for today."

    user_log_text = user_log_entry.user_log

    summary = summarize_user_log(user_log_text)
    return summary
