"""
Campus Router - Handles campus map and location information
"""
from fastapi import APIRouter, HTTPException
from config import CAMPUS_LOCATIONS

router = APIRouter()


@router.get("/locations")
async def get_all_locations():
    """Get all campus locations"""
    return {"locations": CAMPUS_LOCATIONS}


@router.get("/locations/{location_id}")
async def get_location(location_id: str):
    """Get specific campus location"""
    if location_id not in CAMPUS_LOCATIONS:
        raise HTTPException(status_code=404, detail="Location not found")
    return CAMPUS_LOCATIONS[location_id]


@router.get("/categories")
async def get_location_categories():
    """Get location categories"""
    categories = {}
    for loc_id, loc_data in CAMPUS_LOCATIONS.items():
        cat = loc_data["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append({**loc_data, "id": loc_id})
    return categories


@router.get("/search")
async def search_locations(query: str):
    """Search locations by name or description"""
    query_lower = query.lower()
    results = {
        loc_id: loc_data 
        for loc_id, loc_data in CAMPUS_LOCATIONS.items()
        if query_lower in loc_data["name"].lower() or query_lower in loc_data["description"].lower()
    }
    return {"results": results, "count": len(results)}


@router.get("/college-info")
async def get_college_info():
    """Get general college information"""
    return {
        "name": "G. Pulla Reddy Engineering College (Autonomous)",
        "short_name": "GPREC",
        "established": 1997,
        "location": "Kurnool, Andhra Pradesh",
        "affiliated_to": "JNTUA",
        "website": "www.gprec.ac.in",
        "contact": "08518-220010",
        "email": "principal@gprec.ac.in",
        "departments": ["CSE", "ECE", "EEE", "Mechanical", "Civil", "IT", "MBA", "MCA"],
        "total_strength": "~4000 students",
        "accreditation": "NAAC A+ Grade, NBA Accredited",
        "facilities": [
            "Central Library", "Boys & Girls Hostels", "Sports Complex",
            "Medical Center", "Canteen", "ATM", "Wi-Fi Campus"
        ]
    }
