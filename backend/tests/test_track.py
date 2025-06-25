import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

def test_add_track_to_playlist(client, test_db, auth_headers, create_test_playlist, create_test_track):
    playlist = create_test_playlist()
    track = create_test_track(playlist["id"])
    assert track["name"] == "Test Track"

def test_add_track_to_nonexistent_playlist(client, test_db, auth_headers,create_test_playlist):
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

def test_remove_track(client, test_db, auth_headers, create_test_playlist, create_test_track):
    playlist = create_test_playlist()
    track = create_test_track(playlist["id"])
    
    # Remove the track
    resp = client.delete(
        f"/track/{playlist['id']}/tracks/{track['id']}",
        headers=auth_headers
    )
    assert resp.status_code == 204

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
    with patch('routes.track.search_youtube_video') as mock_search:
        # Mock successful YouTube search with just video_id
        mock_search.return_value = "fJ9rUzIMcZQ"  # Changed to match route's response format
        
        resp = client.get("/track/youtube-track", params={
            "track_title": "Bohemian Rhapsody",
            "artist": "Queen"
        })
        
        assert resp.status_code == 200
        result = resp.json()
        assert "video_id" in result, f"Expected video_id in response, got: {result}"
        assert result["video_id"] == "fJ9rUzIMcZQ"

def test_remove_nonexistent_track(client, test_db, auth_headers, create_test_playlist):
    playlist = create_test_playlist()
    playlist_id = playlist["id"]
    
    # Try to remove non-existent track
    resp = client.delete(
        f"/track/{playlist_id}/tracks/999",
        headers=auth_headers
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Track not found in playlist"
