from database import get_user_habits_for_date
from openai_service import summarize_user_log

def generate_daily_summary(user_id: int, target_date):
    # 1. Pull today's habit data
    habits = get_user_habits_for_date(user_id=user_id, date=target_date)
    
    if not habits:
        return "No habits found for today."

    # 2. Build a simple text log
    habits_text = "\n".join(f"- {habit.habit_name}: {habit.status}" for habit in habits)

    # 3. Call your OpenAI summarizer
    summary = summarize_user_log(habits_text)
    return summary
