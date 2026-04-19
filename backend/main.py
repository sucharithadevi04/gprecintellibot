"""
GPREC IntelliBot - FastAPI Backend
AI-Powered Navigator and Information Hub for Students
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging

from routers import chat, placement, notifications, campus
from database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GPREC IntelliBot API",
    description="AI-Powered Navigator and Information Hub for Students at GPREC",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(placement.router, prefix="/api/placement", tags=["Placement"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(campus.router, prefix="/api/campus", tags=["Campus"])


@app.on_event("startup")
async def startup_event():
    logger.info("Starting GPREC IntelliBot API...")
    init_db()
    logger.info("Database initialized successfully.")


@app.get("/")
async def root():
    return {
        "message": "Welcome to GPREC IntelliBot API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "GPREC IntelliBot"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
