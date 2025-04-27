from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

from app.schemas.daily_log_schema import DailyLogRequest
from app.schemas.response_schema import SummarizeResponse, SubmitLogResponse, LogsResponse
from app.core.database import get_db
from app.models.daily_log import DailyLog
from app.services.daily_log_service import generate_daily_summary
from app.services.openai_service import summarize_user_log

router = APIRouter()

# 🛠️ 1. Update /summarize with response_model
@router.post("/summarize", response_model=SummarizeResponse)
def summarize_log(request: DailyLogRequest, db: Session = Depends(get_db)):
    ai_summary = summarize_user_log(request.log_text)

    db_log = DailyLog(
        user_id=request.user_id,
        user_log=request.log_text,
        ai_summary=ai_summary
    )

    try:
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {"summary": ai_summary}


# 🛠️ 2. Update /logs with response_model
@router.get("/logs", response_model=LogsResponse)
def get_logs(limit: int = 10, db: Session = Depends(get_db)):
    logs = db.query(DailyLog).order_by(DailyLog.created_at.desc()).limit(limit).all()
    return logs


# 🛠️ 3. Update /generate-summary with response_model
@router.post("/generate-summary", response_model=SummarizeResponse)
async def generate_summary(user_id: int, db: Session = Depends(get_db)):
    try:
        today = date.today()
        summary = generate_daily_summary(user_id=user_id, target_date=today, db=db)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🛠️ 4. Update /submit-daily-log with response_model
@router.post("/submit-daily-log", response_model=SubmitLogResponse)
async def submit_daily_log(user_id: int, user_log: str, ai_summary: str, db: Session = Depends(get_db)):
    new_log = DailyLog(
        user_id=user_id,
        user_log=user_log,
        ai_summary=ai_summary
    )

    try:
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {
        "message": "Daily log submitted successfully",
        "log_id": new_log.id
    }


# (health check stays simple, no response_model needed)
@router.get("/health")
def health_check():
    return {"status": "ok"}
