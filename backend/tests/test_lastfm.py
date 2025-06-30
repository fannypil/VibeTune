import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

def test_get_lastfm_top_tracks(client, test_db):
    with patch('routes.lastfm.get_lastfm_top_tracks') as mock_top_tracks:
        # Mock the LastFM API response
        mock_top_tracks.return_value = [
            {
                "name": "Test Track",
                "artist": {"name": "Test Artist"},
                # image is not used by the route, so can be omitted
            }
        ]
        
        resp = client.get("/lastfm-top-tracks")
        assert resp.status_code == 200
        assert resp.json()["results"][0]["title"] == "Test Track"
        assert resp.json()["results"][0]["artist"] == "Test Artist"

def test_search_tracks(client, test_db):
    with patch('routes.lastfm.search_lastfm_tracks') as mock_search:
        mock_search.return_value = [
            {
                "name": "Found Track",
                "artist": "Found Artist",
                "url": "http://example.com/found"
            }
        ]
        
        resp = client.get("/search?q=test")
        assert resp.status_code == 200
        assert resp.json()["results"][0]["title"] == "Found Track"
        assert resp.json()["results"][0]["artist"] == "Found Artist"

def test_get_lastfm_top_artists(client, test_db):
    with patch('routes.lastfm.get_lastfm_top_artists') as mock_artists:
        mock_artists.return_value = [{
            "name": "Test Artist",
            "playcount": "1000",
            "listeners": "500",
            "mbid": "test-mbid",
            "url": "http://example.com/artist",
            "streamable": "1",
            "image": "https://cdn-images.dzcdn.net/images/cover/272cc67ce5d91682cc7281f171241f6c/250x250-000000-80-0-0.jpg"
            
        }]
        
        resp = client.get("/lastfm-top-artists")
        assert resp.status_code == 200
        artist = resp.json()[0]
        assert artist["name"] == "Test Artist"
        assert artist["playcount"] == 1000

def test_get_tracks_by_genre(client, test_db):
    with patch('routes.lastfm.get_tracks_by_tags') as mock_genre:
        # Mock LastFM genre response
        mock_genre.return_value = [{
            "name": "Genre Track",  # <-- should be 'name'
            "artist": {"name": "Genre Artist"},
            # 'image' is not used by the route, so can be omitted
        }]
        
        resp = client.get("/genre/pop", params={"limit": 20}) 
        assert resp.status_code == 200, f"Request failed with status {resp.status_code}: {resp.text}"
        
        tracks = resp.json()
        assert len(tracks) > 0
        track = tracks[0]
        assert track["title"] == "Genre Track"
        assert track["artist"] == "Genre Artist"
        
def test_lastfm_api_error(client, test_db):
    with patch('routes.lastfm.get_lastfm_top_tracks') as mock_error:
        mock_error.side_effect = Exception("API Error")
        
        resp = client.get("/lastfm-top-tracks")
        assert resp.status_code == 200
        assert resp.json()["results"] == []  # Empty results
        assert resp.json()["error"] == "API Error"  # Error message included

def test_invalid_genre_limit(client, test_db):
    resp = client.get("/genre/rock?limit=51")  # Over maximum limit
    assert resp.status_code == 422  # Validation error