import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """FastAPI test client fixture."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the activities dictionary to its initial state before each test."""
    # Store the original activities data
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Practice teamwork and compete in friendly soccer matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
        },
        "Swimming Team": {
            "description": "Swim training and conditioning for competitive events",
            "schedule": "Mondays, Wednesdays, 5:00 PM - 6:30 PM",
            "max_participants": 18,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        },
        "Art Workshop": {
            "description": "Explore painting, drawing, and mixed media art projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["grace@mergington.edu", "chloe@mergington.edu"]
        },
        "Drama Society": {
            "description": "Participate in theatre productions and acting exercises",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 20,
            "participants": ["nathan@mergington.edu", "zoe@mergington.edu"]
        },
        "Debate Team": {
            "description": "Practice public speaking and debate current issues",
            "schedule": "Mondays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["isabella@mergington.edu", "jack@mergington.edu"]
        },
        "Math Olympiad Club": {
            "description": "Solve challenging math problems and prepare for competitions",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["oliver@mergington.edu", "emma@mergington.edu"]
        }
    }
    
    # Reset the activities dictionary
    activities.clear()
    activities.update(original_activities)
    yield