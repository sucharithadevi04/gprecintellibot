"""
Database setup using SQLite for GPREC IntelliBot
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_message = Column(Text)
    bot_response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    language = Column(String, default="en")


class StudentProfile(Base):
    __tablename__ = "student_profiles"
    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String)
    roll_number = Column(String, unique=True, index=True)
    branch = Column(String)
    cgpa = Column(Float)
    year = Column(Integer)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    message = Column(Text)
    category = Column(String)  # exam, placement, event, general
    target_branch = Column(String, default="ALL")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)


class PlacementRecord(Base):
    __tablename__ = "placement_records"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    year = Column(Integer)
    students_placed = Column(Integer)
    package_lpa = Column(Float)
    branch = Column(String)


def init_db():
    Base.metadata.create_all(bind=engine)
    _seed_notifications()


def _seed_notifications():
    db = SessionLocal()
    try:
        count = db.query(Notification).count()
        if count == 0:
            sample_notifications = [
                Notification(
                    title="Campus Recruitment Drive - TCS",
                    message="TCS is conducting a campus recruitment drive on March 15, 2025. All eligible students with CGPA >= 6.0 must register at the placement cell before March 10.",
                    category="placement",
                    target_branch="ALL"
                ),
                Notification(
                    title="Mid Semester Examinations",
                    message="Mid semester examinations for III year students will commence from February 20, 2025. Timetable available on the notice board.",
                    category="exam",
                    target_branch="ALL"
                ),
                Notification(
                    title="National Level Tech Fest - GPREC TECHNOVISTA 2025",
                    message="Register now for GPREC TECHNOVISTA 2025 - a national level technical festival on March 5-7, 2025. Events include coding, robotics, paper presentations.",
                    category="event",
                    target_branch="ALL"
                ),
                Notification(
                    title="Library Book Return Reminder",
                    message="Please return all borrowed books before February 28, 2025 to avoid fines. Library working hours: 8 AM - 8 PM on weekdays.",
                    category="general",
                    target_branch="ALL"
                ),
                Notification(
                    title="Infosys InfyTQ Campus Drive",
                    message="Infosys InfyTQ platform registration open for CSE, IT students. Complete certification to be eligible for Infosys campus drive.",
                    category="placement",
                    target_branch="CSE"
                ),
            ]
            for notif in sample_notifications:
                db.add(notif)
            db.commit()
    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
