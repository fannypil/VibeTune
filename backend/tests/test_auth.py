from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_and_login(client, test_db):
    # Test registration with unique username
    resp = client.post("/auth/register", json={
        "username": "testuser123",  # Make username more unique
        "email": "test1@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "Password123"
    })
    assert resp.status_code == 200
    assert resp.json()["email"] == "test1@example.com"

    # Test login
    login = client.post("/auth/login", data={
        "username": "test1@example.com",
        "password": "Password123"
    })
    assert login.status_code == 200
    assert "access_token" in login.json()

def test_register_duplicate_email(client, test_db):
    # Register first user
    resp = client.post("/auth/register", json={
        "username": "testuser1",
        "email": "test2@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "Password123"
    })
    assert resp.status_code == 200

    # Try to register with same email but different username
    resp2 = client.post("/auth/register", json={
        "username": "testuser2",
        "email": "test2@example.com",
        "first_name": "Test2",
        "last_name": "User2",
        "password": "Password123"
    })
    assert resp2.status_code == 400
    assert "Email already registered" in resp2.json()["detail"]

def test_login_with_wrong_password(client, test_db):
    # Register user first
    resp = client.post("/auth/register", json={
        "username": "testuser3",
        "email": "test3@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "Password123"
    })
    assert resp.status_code == 200

    # Try to login with wrong password
    login = client.post("/auth/login", data={
        "username": "test3@example.com",
        "password": "WrongPassword123"
    })
    assert login.status_code == 401
    assert "Incorrect email or password" in login.json()["detail"]

def test_login_nonexistent_user(client, test_db):
    login = client.post("/auth/login", data={
        "username": "nonexistent@example.com",
        "password": "Password123"
    })
    assert login.status_code == 401
    assert "Incorrect email or password" in login.json()["detail"]

def test_register_invalid_email(client, test_db):
    resp = client.post("/auth/register", json={
        "username": "testuser4",
        "email": "invalid-email",
        "first_name": "Test",
        "last_name": "User",
        "password": "Password123"
    })
    assert resp.status_code == 422  # Validation error

def test_register_weak_password(client, test_db):
    resp = client.post("/auth/register", json={
        "username": "testuser5",
        "email": "test5@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "weak"  # Too short, no numbers, no uppercase
    })
    assert resp.status_code == 422

def test_duplicate_username(client, test_db):
    # Register first user
    resp = client.post("/auth/register", json={
        "username": "sameuser",
        "email": "user1@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "Password123"
    })
    assert resp.status_code == 200

    # Try to register with same username but different email 
    resp2 = client.post("/auth/register", json={
        "username": "sameuser",
        "email": "user2@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "Password123"
    })
    assert resp2.status_code == 400
    assert "Username already registered" in resp2.json()["detail"]