# 1. Imports
from fastapi import FastAPI, Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .services.openai_service import summarize_user_log
from .core_database import SessionLocal, engine
from .models import Base, DailyLog
from datetime import date
from .services.services import generate_daily_summary

# 2. Database setup
Base.metadata.create_all(bind=engine)

# 3. Create FastAPI app
app = FastAPI()

# 4. Request Models
class DailyLogRequest(BaseModel):
    log_text: str

# 5. Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 6. Routes
@app.post("/summarize")
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
@app.get("/logs")
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
@app.post("/generate-summary")
async def generate_summary(user_id: int):
    try:
        today = date.today()
        summary = generate_daily_summary(user_id=user_id, target_date=today)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 9. Submit daily log
@app.post("/submit-daily-log")
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