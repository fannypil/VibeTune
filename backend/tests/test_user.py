import pytest
from fastapi.testclient import TestClient
from main import app

def test_read_user(client, test_db):
    # First create a user
    resp = client.post("/auth/register", json={
        "username": "testuser1",
        "email": "test1@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "Password123"
    })
    assert resp.status_code == 200
    user_id = resp.json()["id"]
    
    # Test getting the user by ID
    resp = client.get(f"/users/{user_id}")
    assert resp.status_code == 200
    assert resp.json()["email"] == "test1@example.com"
    assert resp.json()["username"] == "testuser1"
    assert "password" not in resp.json()

def test_read_nonexistent_user(client, test_db):
    resp = client.get("/users/999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "User not found"

def test_read_users_list(client, test_db):
    # Create multiple users
    users = [
        {
            "username": f"testuser{i}",
            "email": f"test{i}@example.com",
            "first_name": f"Test{i}",
            "last_name": "User",
            "password": "Password123"
        }
        for i in range(3)
    ]
    
    for user in users:
        resp = client.post("/auth/register", json=user)
        assert resp.status_code == 200
    
    # Test getting user list
    resp = client.get("/users/")
    assert resp.status_code == 200
    assert len(resp.json()) >= 3
    
    # Test pagination
    resp = client.get("/users/?skip=1&limit=2")
    assert resp.status_code == 200
    assert len(resp.json()) == 2

def test_delete_user(client, test_db):
    # Create a user
    resp = client.post("/auth/register", json={
        "username": "deleteuser",
        "email": "delete@example.com",
        "first_name": "Delete",
        "last_name": "User",
        "password": "Password123"
    })
    assert resp.status_code == 200
    user_id = resp.json()["id"]
    
    # Delete the user
    resp = client.delete(f"/users/{user_id}")
    assert resp.status_code == 204
    
    # Verify user is deleted
    resp = client.get(f"/users/{user_id}")
    assert resp.status_code == 404

def test_delete_nonexistent_user(client, test_db):
    resp = client.delete("/users/999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "User not found"

