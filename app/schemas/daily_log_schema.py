# schemas/daily_log_schema.py

from pydantic import BaseModel

class DailyLogRequest(BaseModel):
    log_text: str
