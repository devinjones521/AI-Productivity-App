# app.py

from fastapi import FastAPI
from pydantic import BaseModel
from services.openai_service import summarize_user_log

# Create FastAPI app
app = FastAPI()

# Define the request model
class DailyLogRequest(BaseModel):
    log_text: str

# Define the POST endpoint
@app.post("/summarize")
def summarize_log(request: DailyLogRequest):
    ai_summary = summarize_user_log(request.log_text)
    return {"summary": ai_summary}
