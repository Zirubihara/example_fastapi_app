import pytest
from fastapi.testclient import TestClient

from app.models.user import User


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(
        name="Test",
        surname="User",
        email="test.user@example.com"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_create_user_success(client: TestClient, api_v1_prefix: str):
    """Test creating user successfully."""
    user_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com"
    }
    response = client.post(f"{api_v1_prefix}/users/", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]


def test_create_user_invalid_email(client: TestClient, api_v1_prefix: str):
    """Test creating user with invalid email."""
    user_data = {
        "name": "John",
        "surname": "Doe",
        "email": "invalid-email"
    }
    response = client.post(f"{api_v1_prefix}/users/", json=user_data)
    assert response.status_code == 422


def test_get_users(client: TestClient, api_v1_prefix: str, test_user: User):
    """Test getting all users."""
    response = client.get(f"{api_v1_prefix}/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 1
    assert any(user["email"] == test_user.email for user in users)


def test_get_user_by_id(client: TestClient, api_v1_prefix: str, test_user: User):
    """Test getting user by ID."""
    response = client.get(f"{api_v1_prefix}/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email


def test_get_user_not_found(client: TestClient, api_v1_prefix: str):
    """Test getting non-existent user."""
    response = client.get(f"{api_v1_prefix}/users/999")
    assert response.status_code == 404 