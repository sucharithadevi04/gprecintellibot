"""
Placement Router - Handles placement analysis and company eligibility
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from database import get_db, StudentProfile
from gemini_service import analyze_student_for_placement
from config import PLACEMENT_COMPANIES

router = APIRouter()


class StudentData(BaseModel):
    name: str
    branch: str
    cgpa: float
    year: int
    skills: Optional[List[str]] = []
    backlogs: Optional[int] = 0
    roll_number: Optional[str] = None
    email: Optional[str] = None


@router.post("/analyze")
async def analyze_placement(student: StudentData, db: Session = Depends(get_db)):
    """Analyze student profile for placement eligibility"""
    student_dict = student.dict()
    result = await analyze_student_for_placement(student_dict)
    
    # Save student profile
    if student.roll_number:
        existing = db.query(StudentProfile).filter(
            StudentProfile.roll_number == student.roll_number
        ).first()
        if not existing:
            profile = StudentProfile(
                student_name=student.name,
                roll_number=student.roll_number,
                branch=student.branch,
                cgpa=student.cgpa,
                year=student.year,
                email=student.email or ""
            )
            db.add(profile)
            db.commit()
    
    return result


@router.get("/companies")
async def get_all_companies():
    """Get list of all placement companies"""
    return {"companies": PLACEMENT_COMPANIES}


@router.get("/companies/filter")
async def filter_companies(branch: str, cgpa: float):
    """Filter companies by branch and CGPA"""
    eligible = [
        c for c in PLACEMENT_COMPANIES
        if cgpa >= c["min_cgpa"] and branch in c["branches"]
    ]
    return {
        "eligible_companies": eligible,
        "count": len(eligible),
        "branch": branch,
        "cgpa": cgpa
    }


@router.get("/stats")
async def placement_stats():
    """Get placement statistics"""
    return {
        "total_companies_visited_2024": 45,
        "total_students_placed_2024": 312,
        "highest_package_lpa": 30.0,
        "average_package_lpa": 5.2,
        "placement_percentage": 78.5,
        "top_recruiters": ["TCS", "Infosys", "Cognizant", "Wipro", "Accenture"],
        "branches_100_percent": ["CSE", "IT"]
    }
