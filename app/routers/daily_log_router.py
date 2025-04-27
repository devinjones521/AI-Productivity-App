# routers/daily_log_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.daily_log_schema import DailyLogRequest
from app.core.database import get_db
from app.models.daily_log import DailyLog
from app.services.daily_log_service import generate_daily_summary
from app.services.openai_service import summarize_user_log
from datetime import date

router = APIRouter()

# 6. Routes
@router.post("/summarize")
def summarize_log(request: DailyLogRequest, db: Session = Depends(get_db)):
    ai_summary = summarize_user_log(request.log_text)

    # Create a new DailyLog record
    db_log = DailyLog(
        user_log=request.log_text,
        ai_summary=ai_summary
    )

    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    return {"summary": ai_summary}

#7. Get all logs
@router.get("/logs")
def get_logs(limit: int = 10, db: Session = Depends(get_db)):
    logs = db.query(DailyLog).order_by(DailyLog.created_at.desc()).limit(limit).all()
    return [
        {
            "id": log.id,
            "user_log": log.user_log,
            "ai_summary": log.ai_summary,
            "created_at": log.created_at
        }
        for log in logs
    ]

# 8. Generate daily summary
@router.post("/generate-summary")
async def generate_summary(user_id: int, db: Session = Depends(get_db)):
    try:
        today = date.today()
        summary = generate_daily_summary(user_id=user_id, target_date=today, db=db)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 9. Submit daily log
@router.post("/submit-daily-log")
async def submit_daily_log(user_id: int, user_log: str, ai_summary: str, db: Session = Depends(get_db)):
    new_log = DailyLog(
        user_id=user_id,
        user_log=user_log,
        ai_summary=ai_summary
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return {"message": "Daily log submitted successfully", "log_id": new_log.id}