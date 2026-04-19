"""
Chat Router - Handles all chat/conversation endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

from database import get_db, ChatHistory
from gemini_service import get_chat_response, get_navigation_help

router = APIRouter()

# In-memory session storage for conversation history
chat_sessions = {}


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    language: Optional[str] = "en"  # en, te, hi


class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str


class NavigationRequest(BaseModel):
    from_location: str
    to_location: str


@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest, db: Session = Depends(get_db)):
    """Send a message to IntelliBot and get AI response"""
    # Generate or use existing session ID
    session_id = request.session_id or str(uuid.uuid4())
    
    # Get conversation history
    history = chat_sessions.get(session_id, [])
    
    # Get AI response
    response_text = await get_chat_response(
        request.message, 
        history, 
        request.language
    )
    
    # Update session history
    history.append({"user": request.message, "bot": response_text})
    chat_sessions[session_id] = history[-10:]  # Keep last 10 exchanges
    
    # Save to database
    chat_record = ChatHistory(
        session_id=session_id,
        user_message=request.message,
        bot_response=response_text,
        language=request.language
    )
    db.add(chat_record)
    db.commit()
    
    return ChatResponse(
        response=response_text,
        session_id=session_id,
        timestamp=datetime.utcnow().isoformat()
    )


@router.get("/history/{session_id}")
async def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    """Get conversation history for a session"""
    records = db.query(ChatHistory).filter(
        ChatHistory.session_id == session_id
    ).order_by(ChatHistory.timestamp).all()
    
    return [
        {
            "user": r.user_message,
            "bot": r.bot_response,
            "timestamp": r.timestamp.isoformat(),
            "language": r.language
        }
        for r in records
    ]


@router.post("/navigate")
async def navigate(request: NavigationRequest):
    """Get navigation help between campus locations"""
    directions = await get_navigation_help(request.from_location, request.to_location)
    return {"directions": directions}


@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear a chat session"""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
    return {"message": "Session cleared successfully"}
