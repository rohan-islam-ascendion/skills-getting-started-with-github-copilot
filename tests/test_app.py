"""Tests for the Mergington High School API."""

import pytest


class TestActivitiesEndpoint:
    """Test cases for GET /activities endpoint."""

    def test_get_activities_success(self, client):
        """Test successful retrieval of all activities."""
        # Arrange
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Soccer Club",
            "Swimming Team", "Art Workshop", "Drama Society", "Debate Team",
            "Math Olympiad Club"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9
        assert all(activity in data for activity in expected_activities)

        # Verify structure of first activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)


class TestSignupEndpoint:
    """Test cases for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client):
        """Test successful signup for an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Signed up {email} for {activity_name}" in data["message"]

        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_activity_not_found(self, client):
        """Test signup for non-existent activity."""
        # Arrange
        activity_name = "NonExistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_participant(self, client):
        """Test signup when student is already registered."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Student already signed up for this activity" in data["detail"]


class TestUnregisterEndpoint:
    """Test cases for DELETE /activities/{activity_name}/participants endpoint."""

    def test_unregister_success(self, client):
        """Test successful unregister from an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.delete(f"/activities/{activity_name}/participants?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Unregistered {email} from {activity_name}" in data["message"]

        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_activity_not_found(self, client):
        """Test unregister from non-existent activity."""
        # Arrange
        activity_name = "NonExistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants?email={email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_participant_not_found(self, client):
        """Test unregister when student is not signed up."""
        # Arrange
        activity_name = "Chess Club"
        email = "notsignedup@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants?email={email}")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Student is not signed up for this activity" in data["detail"]


class TestRootEndpoint:
    """Test cases for GET / endpoint."""

    def test_root_redirect(self, client):
        """Test that root endpoint redirects to static index."""
        # Arrange & Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"


class TestDataIntegrity:
    """Test cases for data integrity and business logic."""

    def test_signup_prevents_duplicates_in_same_activity(self, client):
        """Test that a student cannot sign up twice for the same activity."""
        # Arrange
        activity_name = "Programming Class"
        email = "unique@mergington.edu"

        # Act - First signup
        response1 = client.post(f"/activities/{activity_name}/signup?email={email}")
        # Act - Second signup attempt
        response2 = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400

        # Verify only one instance in participants
        activities_response = client.get("/activities")
        activities = activities_response.json()
        count = activities[activity_name]["participants"].count(email)
        assert count == 1

    def test_participants_list_integrity(self, client):
        """Test that participants list is properly maintained."""
        # Arrange
        activity_name = "Gym Class"
        email1 = "test1@mergington.edu"
        email2 = "test2@mergington.edu"

        # Act - Add participants
        client.post(f"/activities/{activity_name}/signup?email={email1}")
        client.post(f"/activities/{activity_name}/signup?email={email2}")

        # Assert - Both added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        participants = activities[activity_name]["participants"]
        assert email1 in participants
        assert email2 in participants

        # Act - Remove one
        client.delete(f"/activities/{activity_name}/participants?email={email1}")

        # Assert - Only one remains
        activities_response = client.get("/activities")
        activities = activities_response.json()
        participants = activities[activity_name]["participants"]
        assert email1 not in participants
        assert email2 in participants