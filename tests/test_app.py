import os
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import app, activities


client = TestClient(app)


def reset_activities():
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_unregister_participant_removes_email():
    reset_activities()

    response = client.delete("/activities/Chess Club/participants/daniel@mergington.edu")

    assert response.status_code == 200
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Removed daniel@mergington.edu from Chess Club"


def test_signup_adds_participant_to_activity():
    reset_activities()

    response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")

    assert response.status_code == 200
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_unregister_participant_returns_404_for_unknown_email():
    reset_activities()

    response = client.delete("/activities/Chess Club/participants/unknown@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
