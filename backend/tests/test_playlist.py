import pytest
from fastapi.testclient import TestClient
from main import app

def test_create_playlist(client, test_db, auth_headers,create_test_playlist):
    playlist = create_test_playlist()
    assert playlist["name"] == "Test Playlist"
    assert playlist["description"] == "Test playlist description"
    assert "id" in playlist

def test_get_playlist(client, test_db, auth_headers,create_test_playlist):
    playlist = create_test_playlist()
    playlist_id = playlist["id"]

    # Get the playlist
    resp = client.get(f"/playlist/{playlist_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Test Playlist"
    assert "is_favorite" in resp.json()

def test_update_playlist(client, test_db, auth_headers, create_test_playlist):
    playlist = create_test_playlist("Original Name", "Original description")
    playlist_id = playlist["id"]

    # Update the playlist
    update_data = {
        "name": "Updated Name",
        "description": "Updated description"
    }
    resp = client.put(f"/playlist/{playlist_id}", json=update_data, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated Name"

def test_delete_playlist(client, test_db, auth_headers, create_test_playlist):
    playlist = create_test_playlist("To Delete", "Will be deleted")
    playlist_id = playlist["id"]

    # Delete the playlist
    resp = client.delete(f"/playlist/{playlist_id}", headers=auth_headers)
    assert resp.status_code == 204

    # Verify playlist is deleted
    get_resp = client.get(f"/playlist/{playlist_id}", headers=auth_headers)
    assert get_resp.status_code == 404

def test_favorite_playlist(client, test_db, auth_headers, create_test_playlist):
    playlist = create_test_playlist("Favorite Test", "Testing favorites")
    playlist_id = playlist["id"]

    # Favorite the playlist
    resp = client.post(f"/playlist/{playlist_id}/favorite", headers=auth_headers)
    assert resp.status_code == 204

def test_get_my_playlists(client, test_db, auth_headers, create_test_playlist):
    # Create multiple playlists
    playlists = [
        create_test_playlist(f"My Playlist {i}", f"Test {i}")
        for i in range(2)
    ]

    # Get my playlists
    resp = client.get("/playlist/my-playlists", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 2

def test_unauthorized_access(client, test_db):
    # Try to access endpoints without authentication
    endpoints = [
        ("/playlist/", "POST"),
        ("/playlist/1", "GET"),
        ("/playlist/1", "PUT"),
        ("/playlist/1", "DELETE"),
        ("/playlist/my-playlists", "GET"),
        ("/playlist/favorites", "GET")
    ]
    
    for endpoint, method in endpoints:
        if method == "POST":
            resp = client.post(endpoint, json={"name": "Test", "description": "Test"})
        elif method == "PUT":
            resp = client.put(endpoint, json={"name": "Test", "description": "Test"})
        elif method == "DELETE":
            resp = client.delete(endpoint)
        else:
            resp = client.get(endpoint)
            
        assert resp.status_code == 401
        assert resp.json()["detail"] == "Not authenticated"