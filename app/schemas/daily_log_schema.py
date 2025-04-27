# schemas/daily_log_schema.py

from pydantic import BaseModel

class DailyLogRequest(BaseModel):
    user_id: int   # 👈 add this
    log_text: str
