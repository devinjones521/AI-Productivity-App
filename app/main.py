# app/main.py

from fastapi import FastAPI
from app.routers import daily_log_router
from app.core.database import engine
from app.models.daily_log import Base

# 1. Create database tables
Base.metadata.create_all(bind=engine)

# 2. Create FastAPI app
app = FastAPI()

# 3. Include routers
app.include_router(daily_log_router.router)


