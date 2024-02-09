import pytest
from fastapi.testclient import TestClient

from app.database import Base, test_engine
from app.main import app


class TestUserAPI:
    """
    Class to test users API endpoints
    """

    @pytest.fixture(scope="module")
    def db(self):
        """
        Fixture to set up and tear down the database for testing
        """
        Base.metadata.create_all(bind=test_engine)
        yield
        Base.metadata.drop_all(bind=test_engine)

    @pytest.fixture(scope="module")
    def client(self):
        """
        Fixture to create a test client for the FastAPI app
        """
        with TestClient(app) as test_client:
            yield test_client

    def test_create_user(self, db, client):
        """
        Test the creation of a new user via the API
        """
        user_data = {"username": "test_user", "email": "test@example.com"}
        response = client.post("/users/", json=user_data)
        assert response.status_code == 200
        assert response.json()["username"] == user_data["username"]
        assert response.json()["email"] == user_data["email"]

    def test_get_users(self, db, client):
        """
        Test fetching a list of users via the API
        """
        response = client.get("/users/")
        assert response.status_code == 200
        assert response.json()["users"][0]["email"] == "test@example.com"

    def test_get_user(self, db, client):
        """
        Test fetching a single user by ID via the API
        """
        user_id = 1
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"

    def test_update_user(self, db, client):
        """
        Test updating user information via the API
        """
        user_id = 1
        updated_data = {"username": "updated_user"}
        response = client.patch(f"/users/{user_id}", json=updated_data)
        assert response.status_code == 200
        assert response.json()["username"] == updated_data["username"]

    def test_delete_user(self, db, client):
        """
        Test deleting a user via the API
        """
        user_id = 1
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted successfully"
