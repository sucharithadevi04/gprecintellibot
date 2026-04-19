"""
Gemini AI Service for GPREC IntelliBot
Handles all AI-powered interactions using Google Gemini API
"""
import google.generativeai as genai
from config import settings, COLLEGE_FAQS, CAMPUS_LOCATIONS, PLACEMENT_COMPANIES
import logging

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel(settings.GEMINI_MODEL)

SYSTEM_PROMPT = """You are GPREC IntelliBot, an intelligent AI assistant for G. Pulla Reddy Engineering College (GPREC), Kurnool, Andhra Pradesh, India.

You help students with:
1. Campus navigation and location information
2. Admission procedures and fee details
3. Placement guidance and company eligibility
4. Academic information (exams, schedules, results)
5. Hostel, canteen, library information
6. Scholarships and financial aid
7. Club activities and events
8. General college life queries

College Info:
- Full Name: G. Pulla Reddy Engineering College (Autonomous), Kurnool
- Established: 1997
- Affiliation: JNTUA (Jawaharlal Nehru Technological University Anantapur)
- Website: www.gprec.ac.in
- Contact: 08518-220010
- Location: Kurnool, Andhra Pradesh

Departments: CSE, ECE, EEE, MECH, CIVIL, IT, MBA, MCA

Campus FAQs:
{}

Available Campus Locations: Main Gate, Admin Block, CSE Block, ECE Block, Library, Canteen, Sports Ground, Boys Hostel, Girls Hostel, Placement Cell, Auditorium, Medical Center, ATM

IMPORTANT GUIDELINES:
- Be helpful, friendly, and concise
- If asked in Telugu, respond in Telugu
- If asked in Hindi, respond in Hindi  
- Always maintain a professional yet approachable tone
- For location queries, provide specific directions
- For placement queries, mention CGPA requirements
- Always encourage students and be positive
- If you don't know something specific, direct them to the relevant office
""".format("\n".join([f"- {k}: {v}" for k, v in COLLEGE_FAQS.items()]))


async def get_chat_response(user_message: str, chat_history: list = None, language: str = "en") -> str:
    """Get AI response using Gemini API"""
    try:
        # Build context-aware prompt
        lang_instruction = ""
        if language == "te":
            lang_instruction = "Please respond in Telugu (తెలుగు) language. "
        elif language == "hi":
            lang_instruction = "Please respond in Hindi (हिंदी) language. "

        # Format conversation history
        history_context = ""
        if chat_history and len(chat_history) > 0:
            history_context = "\nConversation History:\n"
            for h in chat_history[-5:]:  # Last 5 messages
                history_context += f"User: {h['user']}\nBot: {h['bot']}\n"

        full_prompt = f"""{SYSTEM_PROMPT}

{history_context}

{lang_instruction}User Query: {user_message}

Provide a helpful, accurate response about GPREC:"""

        response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return "I apologize, I'm having trouble connecting to my AI service right now. Please try again in a moment, or contact the college directly at 08518-220010."


async def analyze_student_for_placement(student_data: dict) -> dict:
    """Analyze student profile for placement eligibility"""
    try:
        eligible_companies = []
        for company in PLACEMENT_COMPANIES:
            if (student_data.get("cgpa", 0) >= company["min_cgpa"] and
                    student_data.get("branch", "") in company["branches"]):
                eligible_companies.append(company)

        prompt = f"""As a placement advisor for GPREC, analyze this student profile and provide personalized advice:

Student Profile:
- Name: {student_data.get('name', 'Student')}
- Branch: {student_data.get('branch', 'N/A')}
- CGPA: {student_data.get('cgpa', 'N/A')}
- Year: {student_data.get('year', 'N/A')}
- Skills: {', '.join(student_data.get('skills', []))}
- Backlogs: {student_data.get('backlogs', 0)}

Eligible Companies: {[c['name'] for c in eligible_companies]}

Provide:
1. Top 3 company recommendations with reasons
2. Skills to improve for better placement chances
3. Short-term preparation advice (next 3 months)
4. Estimated package range

Be encouraging and specific to GPREC students."""

        response = model.generate_content(prompt)
        return {
            "eligible_companies": eligible_companies,
            "ai_advice": response.text,
            "total_eligible": len(eligible_companies)
        }

    except Exception as e:
        logger.error(f"Placement analysis error: {e}")
        return {
            "eligible_companies": eligible_companies if 'eligible_companies' in locals() else [],
            "ai_advice": "Unable to generate AI advice at this time. Please visit the placement cell for personalized guidance.",
            "total_eligible": 0
        }


async def get_navigation_help(from_location: str, to_location: str) -> str:
    """Get navigation directions between campus locations"""
    try:
        locations_info = "\n".join([f"- {k}: {v['description']} (positioned at {v['x']}%, {v['y']}% on map)" 
                                     for k, v in CAMPUS_LOCATIONS.items()])
        
        prompt = f"""As a campus guide for GPREC Kurnool, provide clear walking directions:

From: {from_location}
To: {to_location}

Campus Layout Information:
{locations_info}

Provide step-by-step walking directions in a friendly manner. Include landmarks and approximate walking time. Keep it concise."""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        logger.error(f"Navigation error: {e}")
        return f"To get from {from_location} to {to_location}, please ask any staff member or security guard for directions."
