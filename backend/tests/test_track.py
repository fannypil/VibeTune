import pytest
from fastapi.testclient import TestClient
from main import app

def test_add_track_to_playlist(client, test_db, auth_headers):
    # Create a playlist
    playlist_data = {
        "name": "Test Playlist",
        "description": "Test playlist for tracks"
    }
    resp = client.post("/playlist/", json=playlist_data, headers=auth_headers)
    assert resp.status_code == 200
    playlist_id = resp.json()["id"]
    
    # Add track to playlist
    track_data = {
        "name": "Test Track",
        "artist": "Test Artist",
        "url": "http://example.com/track",
        "playlist_id": playlist_id
    }
    resp = client.post(
        f"/track/{playlist_id}/tracks",
        json=track_data,
        headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Test Track"

def test_add_track_to_nonexistent_playlist(client, test_db, auth_headers):
    track_data = {
        "name": "Test Track",
        "artist": "Test Artist",
        "url": "http://example.com/track",
        "playlist_id": 999
    }
    resp = client.post(
        "/track/999/tracks",
        json=track_data,
        headers=auth_headers
    )
    assert resp.status_code == 404

def test_remove_track(client, test_db, auth_headers):
    # First create a playlist
    playlist_data = {
        "name": "Test Playlist",
        "description": "Test playlist for tracks"
    }
    resp = client.post("/playlist/", json=playlist_data, headers=auth_headers)
    assert resp.status_code == 200
    playlist_id = resp.json()["id"]
    
    # Add a track to the playlist
    track_data = {
        "name": "Test Track",
        "artist": "Test Artist",
        "url": "http://example.com/track",
        "playlist_id": playlist_id
    }
    resp = client.post(
        f"/track/{playlist_id}/tracks",
        json=track_data,
        headers=auth_headers
    )
    assert resp.status_code == 200
    track_id = resp.json()["id"]
    
    # Remove the track
    resp = client.delete(
        f"/track/{playlist_id}/tracks/{track_id}",
        headers=auth_headers
    )
    assert resp.status_code == 204
    
    # Verify track is removed
    resp = client.get(f"/playlist/{playlist_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert track_id not in [t["id"] for t in resp.json()["tracks"]]

def test_remove_track_from_nonexistent_playlist(client, test_db, auth_headers):
    resp = client.delete("/track/999/tracks/1", headers=auth_headers)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Playlist not found"

def test_unauthorized_track_operations(client, test_db):
    # Try operations without authentication
    resp = client.post("/track/1/tracks", json={
        "name": "Test Track",
        "artist": "Test Artist",
        "url": "http://example.com/track",
        "playlist_id": 1
    })
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Not authenticated"

def test_youtube_track_search(client, test_db):
    resp = client.get("/track/youtube-track", params={
        "track_title": "Bohemian Rhapsody",
        "artist": "Queen"
    })
    assert resp.status_code == 200
    assert "video_id" in resp.json()

def test_remove_nonexistent_track(client, test_db, auth_headers):
    # First create a playlist
    playlist_data = {
        "name": "Test Playlist",
        "description": "Test playlist for tracks"
    }
    resp = client.post("/playlist/", json=playlist_data, headers=auth_headers)
    assert resp.status_code == 200
    playlist_id = resp.json()["id"]
    
    # Try to remove non-existent track
    resp = client.delete(
        f"/track/{playlist_id}/tracks/999",
        headers=auth_headers
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Track not found in playlist"