"""
Configuration settings for GPREC IntelliBot
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Gemini API
    GEMINI_API_KEY: str = "AIzaSyAqbv4N7IuhVYOQPEAgWi1DWrgC0RLBTg8"
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # App Settings
    APP_NAME: str = "GPREC IntelliBot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./gprec_intellibot.db"

    # FastAPI
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()

# Campus location data
CAMPUS_LOCATIONS = {
    "main_gate": {
        "name": "Main Gate",
        "x": 50, "y": 90,
        "description": "Main entrance to GPREC campus",
        "category": "entrance"
    },
    "admin_block": {
        "name": "Administrative Block",
        "x": 50, "y": 70,
        "description": "Principal office, exam cell, fee section, all administrative offices",
        "category": "admin"
    },
    "cse_block": {
        "name": "CSE Department",
        "x": 30, "y": 50,
        "description": "Computer Science & Engineering labs, classrooms, faculty rooms",
        "category": "department"
    },
    "ece_block": {
        "name": "ECE Department",
        "x": 70, "y": 50,
        "description": "Electronics & Communication Engineering department",
        "category": "department"
    },
    "library": {
        "name": "Central Library",
        "x": 50, "y": 40,
        "description": "Library with 50,000+ books, journals, digital resources",
        "category": "facility"
    },
    "canteen": {
        "name": "Canteen / Food Court",
        "x": 20, "y": 70,
        "description": "Main canteen with affordable meals and snacks",
        "category": "facility"
    },
    "sports_ground": {
        "name": "Sports Ground",
        "x": 80, "y": 30,
        "description": "Cricket ground, basketball court, volleyball court",
        "category": "sports"
    },
    "hostel_boys": {
        "name": "Boys Hostel",
        "x": 15, "y": 30,
        "description": "Boys residential hostel with mess facility",
        "category": "hostel"
    },
    "hostel_girls": {
        "name": "Girls Hostel",
        "x": 85, "y": 70,
        "description": "Girls residential hostel with mess facility",
        "category": "hostel"
    },
    "placement_cell": {
        "name": "Placement Cell",
        "x": 60, "y": 60,
        "description": "Training & Placement office, interview preparation rooms",
        "category": "placement"
    },
    "mech_block": {
        "name": "Mechanical Engineering",
        "x": 40, "y": 30,
        "description": "Mechanical engineering workshops and labs",
        "category": "department"
    },
    "civil_block": {
        "name": "Civil Engineering",
        "x": 60, "y": 35,
        "description": "Civil engineering department and survey lab",
        "category": "department"
    },
    "auditorium": {
        "name": "Auditorium",
        "x": 50, "y": 55,
        "description": "Main auditorium for college events and seminars",
        "category": "facility"
    },
    "medical_center": {
        "name": "Medical Center",
        "x": 25, "y": 55,
        "description": "On-campus health center with doctor",
        "category": "facility"
    },
    "atm": {
        "name": "ATM",
        "x": 45, "y": 85,
        "description": "SBI ATM near main gate",
        "category": "facility"
    }
}

# Placement companies data
PLACEMENT_COMPANIES = [
    {"name": "TCS", "min_cgpa": 6.0, "branches": ["CSE", "ECE", "IT", "MECH", "CIVIL"], "package_lpa": 3.5, "role": "Software Engineer"},
    {"name": "Infosys", "min_cgpa": 6.5, "branches": ["CSE", "ECE", "IT"], "package_lpa": 3.6, "role": "Systems Engineer"},
    {"name": "Wipro", "min_cgpa": 6.0, "branches": ["CSE", "ECE", "IT", "EEE"], "package_lpa": 3.5, "role": "Project Engineer"},
    {"name": "Cognizant", "min_cgpa": 6.0, "branches": ["CSE", "IT", "ECE"], "package_lpa": 4.0, "role": "Programmer Analyst"},
    {"name": "Accenture", "min_cgpa": 6.5, "branches": ["CSE", "IT", "ECE", "EEE"], "package_lpa": 4.5, "role": "Associate Software Engineer"},
    {"name": "HCL", "min_cgpa": 6.0, "branches": ["CSE", "ECE", "MECH", "EEE"], "package_lpa": 3.2, "role": "Graduate Engineer"},
    {"name": "Tech Mahindra", "min_cgpa": 5.5, "branches": ["CSE", "ECE", "IT"], "package_lpa": 3.5, "role": "Software Developer"},
    {"name": "Capgemini", "min_cgpa": 6.0, "branches": ["CSE", "IT", "ECE"], "package_lpa": 3.8, "role": "Analyst"},
    {"name": "Amazon", "min_cgpa": 7.5, "branches": ["CSE", "IT"], "package_lpa": 15.0, "role": "SDE-1"},
    {"name": "Microsoft", "min_cgpa": 8.0, "branches": ["CSE", "IT"], "package_lpa": 20.0, "role": "Software Engineer"},
    {"name": "Google", "min_cgpa": 8.5, "branches": ["CSE", "IT"], "package_lpa": 30.0, "role": "Software Engineer"},
    {"name": "IBM", "min_cgpa": 6.5, "branches": ["CSE", "ECE", "IT", "EEE"], "package_lpa": 4.2, "role": "Associate Developer"},
    {"name": "Deloitte", "min_cgpa": 6.0, "branches": ["CSE", "IT", "ECE", "EEE", "MECH", "CIVIL"], "package_lpa": 6.0, "role": "Business Technology Analyst"},
    {"name": "KPIT", "min_cgpa": 6.5, "branches": ["MECH", "EEE", "ECE", "CSE"], "package_lpa": 4.5, "role": "Software Engineer"},
    {"name": "Mphasis", "min_cgpa": 6.0, "branches": ["CSE", "IT"], "package_lpa": 3.8, "role": "Junior Developer"},
]

# FAQ data for the chatbot
COLLEGE_FAQS = {
    "admission": "Admissions at GPREC are through EAMCET/ECET counseling. Contact the admission cell at the administrative block or call 08518-220010.",
    "fee_structure": "Fee structure varies by branch. Engineering programs range from ₹35,000 to ₹85,000 per year. Contact the fee section in Admin Block.",
    "exam_schedule": "Exam schedules are published on the college notice board and website www.gprec.ac.in. Internal exams are held twice a semester.",
    "library_timings": "Library is open from 8:00 AM to 8:00 PM on weekdays and 9:00 AM to 5:00 PM on weekends.",
    "hostel": "Both boys and girls hostels are available on campus. Contact the warden at the respective hostel office for availability.",
    "placement": "The Training & Placement cell is located in the Academic Block. Contact placement officer for company visits and schedules.",
    "scholarships": "Various scholarships available including SC/ST, BC, EBC scholarships from AP government. Contact the scholarship section in Admin Block.",
    "canteen": "The main canteen operates from 7:30 AM to 8:00 PM. Meals, snacks, and beverages are available at subsidized rates.",
}
