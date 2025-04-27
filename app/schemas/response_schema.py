from pydantic import BaseModel, RootModel
from datetime import datetime

class SummarizeResponse(BaseModel):
    summary: str

class SubmitLogResponse(BaseModel):
    message: str
    log_id: int

class LogEntry(BaseModel):
    id: int
    user_log: str
    ai_summary: str
    created_at: datetime

class LogsResponse(RootModel[list['LogEntry']]):
    pass
