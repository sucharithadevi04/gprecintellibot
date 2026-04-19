"""
GPREC IntelliBot - Test Cases
Run with: pytest tests/ -v
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock


# ─────────────────────────────────────────────────────────────────────────────
# Setup - patch Gemini before importing app
# ─────────────────────────────────────────────────────────────────────────────
@pytest.fixture(scope="session", autouse=True)
def mock_gemini():
    with patch("google.generativeai.configure"), \
         patch("google.generativeai.GenerativeModel") as mock_model:
        mock_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "This is a mocked AI response from IntelliBot."
        mock_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_instance
        yield mock_model


@pytest.fixture(scope="session")
def client(mock_gemini):
    from main import app
    from database import Base, engine
    Base.metadata.create_all(bind=engine)
    return TestClient(app)


# ─────────────────────────────────────────────────────────────────────────────
# 1. API Health & Root
# ─────────────────────────────────────────────────────────────────────────────
class TestHealthEndpoints:
    def test_root_returns_200(self, client):
        r = client.get("/")
        assert r.status_code == 200

    def test_root_welcome_message(self, client):
        r = client.get("/")
        assert "GPREC IntelliBot" in r.json()["message"]

    def test_health_check(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "healthy"

    def test_health_service_name(self, client):
        r = client.get("/health")
        assert "GPREC IntelliBot" in r.json()["service"]


# ─────────────────────────────────────────────────────────────────────────────
# 2. Chat API
# ─────────────────────────────────────────────────────────────────────────────
class TestChatAPI:
    def test_chat_message_basic(self, client):
        payload = {"message": "Hello, what is GPREC?", "language": "en"}
        r = client.post("/api/chat/message", json=payload)
        assert r.status_code == 200

    def test_chat_message_returns_response(self, client):
        payload = {"message": "Where is the library?"}
        r = client.post("/api/chat/message", json=payload)
        data = r.json()
        assert "response" in data
        assert isinstance(data["response"], str)
        assert len(data["response"]) > 0

    def test_chat_message_returns_session_id(self, client):
        payload = {"message": "Hello"}
        r = client.post("/api/chat/message", json=payload)
        data = r.json()
        assert "session_id" in data
        assert len(data["session_id"]) > 0

    def test_chat_message_returns_timestamp(self, client):
        payload = {"message": "Hello"}
        r = client.post("/api/chat/message", json=payload)
        data = r.json()
        assert "timestamp" in data

    def test_chat_with_session_id(self, client):
        session_id = "test-session-12345"
        payload = {"message": "Hello", "session_id": session_id}
        r = client.post("/api/chat/message", json=payload)
        assert r.status_code == 200
        assert r.json()["session_id"] == session_id

    def test_chat_history_retrieval(self, client):
        session_id = "history-test-session"
        client.post("/api/chat/message", json={"message": "Hi", "session_id": session_id})
        r = client.get(f"/api/chat/history/{session_id}")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_chat_history_has_correct_fields(self, client):
        session_id = "field-test-session"
        client.post("/api/chat/message", json={"message": "Test message", "session_id": session_id})
        r = client.get(f"/api/chat/history/{session_id}")
        record = r.json()[0]
        assert "user" in record
        assert "bot" in record
        assert "timestamp" in record

    def test_chat_telugu_language(self, client):
        payload = {"message": "గ్రంథాలయం ఎక్కడ ఉంది?", "language": "te"}
        r = client.post("/api/chat/message", json=payload)
        assert r.status_code == 200

    def test_chat_clear_session(self, client):
        session_id = "clear-test-session"
        client.post("/api/chat/message", json={"message": "Test", "session_id": session_id})
        r = client.delete(f"/api/chat/session/{session_id}")
        assert r.status_code == 200
        assert "cleared" in r.json()["message"].lower()

    def test_navigation_request(self, client):
        payload = {"from_location": "Main Gate", "to_location": "Library"}
        r = client.post("/api/chat/navigate", json=payload)
        assert r.status_code == 200
        assert "directions" in r.json()


# ─────────────────────────────────────────────────────────────────────────────
# 3. Campus API
# ─────────────────────────────────────────────────────────────────────────────
class TestCampusAPI:
    def test_get_all_locations(self, client):
        r = client.get("/api/campus/locations")
        assert r.status_code == 200
        data = r.json()
        assert "locations" in data
        assert len(data["locations"]) > 0

    def test_locations_have_required_fields(self, client):
        r = client.get("/api/campus/locations")
        locs = r.json()["locations"]
        for loc_id, loc in locs.items():
            assert "name" in loc
            assert "description" in loc
            assert "category" in loc
            assert "x" in loc
            assert "y" in loc

    def test_get_specific_location(self, client):
        r = client.get("/api/campus/locations/library")
        assert r.status_code == 200
        data = r.json()
        assert data["name"] == "Central Library"

    def test_location_not_found(self, client):
        r = client.get("/api/campus/locations/nonexistent_location")
        assert r.status_code == 404

    def test_location_categories(self, client):
        r = client.get("/api/campus/categories")
        assert r.status_code == 200
        data = r.json()
        # Should have multiple categories
        assert len(data) > 1

    def test_location_search(self, client):
        r = client.get("/api/campus/search?query=library")
        assert r.status_code == 200
        data = r.json()
        assert "results" in data
        assert data["count"] >= 1

    def test_location_search_no_results(self, client):
        r = client.get("/api/campus/search?query=xyznonexistent")
        assert r.status_code == 200
        assert r.json()["count"] == 0

    def test_college_info(self, client):
        r = client.get("/api/campus/college-info")
        assert r.status_code == 200
        data = r.json()
        assert "GPREC" in data["short_name"]
        assert data["established"] == 1997

    def test_college_info_has_departments(self, client):
        r = client.get("/api/campus/college-info")
        data = r.json()
        assert "departments" in data
        assert "CSE" in data["departments"]


# ─────────────────────────────────────────────────────────────────────────────
# 4. Placement API
# ─────────────────────────────────────────────────────────────────────────────
class TestPlacementAPI:
    def test_get_all_companies(self, client):
        r = client.get("/api/placement/companies")
        assert r.status_code == 200
        data = r.json()
        assert "companies" in data
        assert len(data["companies"]) > 0

    def test_companies_have_required_fields(self, client):
        r = client.get("/api/placement/companies")
        companies = r.json()["companies"]
        for c in companies:
            assert "name" in c
            assert "min_cgpa" in c
            assert "branches" in c
            assert "package_lpa" in c

    def test_filter_companies_by_branch_cgpa(self, client):
        r = client.get("/api/placement/companies/filter?branch=CSE&cgpa=7.0")
        assert r.status_code == 200
        data = r.json()
        assert "eligible_companies" in data
        # All returned companies should have CSE in branches
        for company in data["eligible_companies"]:
            assert "CSE" in company["branches"]
            assert company["min_cgpa"] <= 7.0

    def test_filter_companies_high_cgpa(self, client):
        r = client.get("/api/placement/companies/filter?branch=CSE&cgpa=9.0")
        data = r.json()
        # High CGPA should return more companies
        assert data["count"] > 0

    def test_filter_companies_low_cgpa(self, client):
        r = client.get("/api/placement/companies/filter?branch=CSE&cgpa=4.0")
        data = r.json()
        # Very low CGPA should return fewer or no companies
        assert data["count"] == 0 or all(c["min_cgpa"] <= 4.0 for c in data["eligible_companies"])

    def test_placement_stats(self, client):
        r = client.get("/api/placement/stats")
        assert r.status_code == 200
        data = r.json()
        assert "total_students_placed_2024" in data
        assert "placement_percentage" in data
        assert "highest_package_lpa" in data

    def test_analyze_student_profile(self, client):
        payload = {
            "name": "Test Student",
            "branch": "CSE",
            "cgpa": 7.5,
            "year": 4,
            "skills": ["Python", "Java"],
            "backlogs": 0
        }
        r = client.post("/api/placement/analyze", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert "eligible_companies" in data
        assert "ai_advice" in data
        assert "total_eligible" in data

    def test_analyze_student_low_cgpa(self, client):
        payload = {
            "name": "Low CGPA Student",
            "branch": "CSE",
            "cgpa": 5.0,
            "year": 3,
            "skills": [],
            "backlogs": 2
        }
        r = client.post("/api/placement/analyze", json=payload)
        assert r.status_code == 200
        # Even low CGPA returns a valid response
        assert "eligible_companies" in r.json()


# ─────────────────────────────────────────────────────────────────────────────
# 5. Notifications API
# ─────────────────────────────────────────────────────────────────────────────
class TestNotificationsAPI:
    def test_get_all_notifications(self, client):
        r = client.get("/api/notifications/")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_notifications_have_required_fields(self, client):
        r = client.get("/api/notifications/")
        notifs = r.json()
        if notifs:
            for n in notifs:
                assert "title" in n
                assert "message" in n
                assert "category" in n

    def test_filter_by_category(self, client):
        r = client.get("/api/notifications/?category=placement")
        assert r.status_code == 200
        notifs = r.json()
        for n in notifs:
            assert n["category"] == "placement"

    def test_filter_by_branch(self, client):
        r = client.get("/api/notifications/?branch=CSE")
        assert r.status_code == 200

    def test_create_notification(self, client):
        payload = {
            "title": "Test Notification",
            "message": "This is a test notification for pytest",
            "category": "general",
            "target_branch": "ALL"
        }
        r = client.post("/api/notifications/", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert "id" in data

    def test_notification_categories(self, client):
        r = client.get("/api/notifications/categories")
        assert r.status_code == 200
        data = r.json()
        assert "categories" in data
        categories = [c["id"] for c in data["categories"]]
        assert "placement" in categories
        assert "exam" in categories


# ─────────────────────────────────────────────────────────────────────────────
# 6. Config & Data Validation
# ─────────────────────────────────────────────────────────────────────────────
class TestConfigAndData:
    def test_campus_locations_not_empty(self):
        from config import CAMPUS_LOCATIONS
        assert len(CAMPUS_LOCATIONS) > 0

    def test_campus_locations_structure(self):
        from config import CAMPUS_LOCATIONS
        for loc_id, loc in CAMPUS_LOCATIONS.items():
            assert "name" in loc, f"{loc_id} missing 'name'"
            assert "x" in loc and "y" in loc, f"{loc_id} missing coordinates"
            assert 0 <= loc["x"] <= 100, f"{loc_id} x out of range"
            assert 0 <= loc["y"] <= 100, f"{loc_id} y out of range"

    def test_placement_companies_not_empty(self):
        from config import PLACEMENT_COMPANIES
        assert len(PLACEMENT_COMPANIES) > 0

    def test_placement_companies_structure(self):
        from config import PLACEMENT_COMPANIES
        for c in PLACEMENT_COMPANIES:
            assert "name" in c
            assert "min_cgpa" in c
            assert "branches" in c
            assert "package_lpa" in c
            assert isinstance(c["branches"], list)
            assert 0 <= c["min_cgpa"] <= 10

    def test_college_faqs_not_empty(self):
        from config import COLLEGE_FAQS
        assert len(COLLEGE_FAQS) > 0

    def test_settings_has_gemini_key(self):
        from config import settings
        assert settings.GEMINI_API_KEY is not None
        assert len(settings.GEMINI_API_KEY) > 10


# ─────────────────────────────────────────────────────────────────────────────
# 7. Edge Cases
# ─────────────────────────────────────────────────────────────────────────────
class TestEdgeCases:
    def test_empty_message_handling(self, client):
        payload = {"message": ""}
        r = client.post("/api/chat/message", json=payload)
        # Should still return 200 (backend handles gracefully)
        assert r.status_code in [200, 422]

    def test_very_long_message(self, client):
        long_msg = "What is GPREC? " * 50
        payload = {"message": long_msg}
        r = client.post("/api/chat/message", json=payload)
        assert r.status_code == 200

    def test_special_characters_in_message(self, client):
        payload = {"message": "What about GPREC's admission? <test> & more?"}
        r = client.post("/api/chat/message", json=payload)
        assert r.status_code == 200

    def test_placement_invalid_cgpa(self, client):
        payload = {"name": "Test", "branch": "CSE", "cgpa": 15.0, "year": 4}
        r = client.post("/api/placement/analyze", json=payload)
        # Should handle gracefully
        assert r.status_code in [200, 422]

    def test_concurrent_sessions(self, client):
        sessions = [f"session-{i}" for i in range(5)]
        responses = []
        for session_id in sessions:
            r = client.post("/api/chat/message", json={
                "message": f"Hello from session {session_id}",
                "session_id": session_id
            })
            responses.append(r.status_code)
        assert all(s == 200 for s in responses)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
