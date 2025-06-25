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
                "url": "http://example.com/track"
            }
        ]
        
        resp = client.get("/lastfm-top-tracks")
        assert resp.status_code == 200
        assert resp.json()["results"][0]["name"] == "Test Track"
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
        assert resp.json()["results"][0]["name"] == "Found Track"
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
            "image": [
                {"#text": "small.jpg", "size": "small"},
                {"#text": "medium.jpg", "size": "medium"},
                {"#text": "large.jpg", "size": "large"},
                {"#text": "extralarge.jpg", "size": "extralarge"},
                {"#text": "mega.jpg", "size": "mega"}
            ]
        }]
        
        resp = client.get("/lastfm-top-artists")
        assert resp.status_code == 200
        artist = resp.json()[0]
        assert artist["name"] == "Test Artist"
        assert artist["playcount"] == 1000
        assert artist["image_large"] == "large.jpg"

def test_get_tracks_by_genre(client, test_db):
    with patch('routes.lastfm.get_tracks_by_tags') as mock_genre:
        # Mock LastFM genre response
        mock_genre.return_value = [{
            "name": "Genre Track",
            "artist": {"name": "Genre Artist"},
            "url": "http://example.com/genre",
            "image": [
                {"#text": "small.jpg", "size": "small"},
                {"#text": "large.jpg", "size": "large"}
            ]           
        }]
        
        resp = client.get("/genre/rock", params={"limit": 20}) 
        assert resp.status_code == 200, f"Request failed with status {resp.status_code}: {resp.text}"
        
        tracks = resp.json()
        assert len(tracks) > 0
        track = tracks[0]
        assert track["title"] == "Genre Track"
        assert track["artist"] == "Genre Artist"
        assert track.get("url") == "http://example.com/genre"
        assert track.get("image") == "large.jpg"  # Should get the largest image
        
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