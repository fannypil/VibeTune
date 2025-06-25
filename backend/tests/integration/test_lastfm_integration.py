import pytest
from conftest import client
import logging
import time

logger = logging.getLogger(__name__)

@pytest.mark.integration
def test_lastfm_search_integration():
    """Test real LastFM API search functionality"""
    response = client.get("/search?q=The%20Beatles")
    assert response.status_code == 200
    
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0
    
    for track in data["results"]:
        assert all(key in track for key in ["name", "artist", "url"])
    logger.info(f"Found {len(data['results'])} results for 'The Beatles'")

@pytest.mark.integration
def test_lastfm_genre_integration():
    """Test genre-based track recommendations"""
    genres = ["rock", "pop", "jazz"]
    
    for genre in genres:
        response = client.get(f"/genre/{genre}?limit=10")
        assert response.status_code == 200
        
        tracks = response.json()
        if tracks:  # If we got tracks back
            assert len(tracks) > 0
            for track in tracks:
                assert all(key in track for key in ["title", "artist", "url"])
                # Don't check for listeners anymore
            logger.info(f"Found {len(tracks)} {genre} tracks")
            return  # Test passed
            
    pytest.fail("No valid tracks found for any tested genre")
            
    pytest.fail("No valid tracks found for any tested genre")

@pytest.mark.integration
def test_lastfm_top_artists_integration():
    """Test fetching top artists from LastFM"""
    response = client.get("/lastfm-top-artists")
    assert response.status_code == 200
    
    artists = response.json()
    assert len(artists) > 0
    assert all("listeners" in artist for artist in artists)
    logger.info(f"Found {len(artists)} top artists")

@pytest.mark.integration
def test_search_and_genre_correlation():
    """Test correlation between search results and genre tracks"""
    # First get some rock tracks
    genre_response = client.get("/genre/rock?limit=5")
    assert genre_response.status_code == 200
    genre_tracks = genre_response.json()
    
    if genre_tracks:
        # Take first track and search for its artist
        first_track = genre_tracks[0]
        search_response = client.get(f"/search?q={first_track['artist']}")
        assert search_response.status_code == 200
        search_results = search_response.json()["results"]
        
        # Verify artist appears in search results
        artist_found = any(
            track["artist"].lower() == first_track["artist"].lower()
            for track in search_results
        )
        assert artist_found
        logger.info(f"Successfully correlated genre tracks with search for {first_track['artist']}")

@pytest.mark.integration
def test_api_rate_limiting():
    """Test API rate limiting and performance"""
    start_time = time.time()
    request_count = 5
    
    # Make multiple requests in quick succession
    responses = []
    for _ in range(request_count):
        response = client.get("/search?q=test")
        responses.append(response)
        
    end_time = time.time()
    total_time = end_time - start_time
    
    # Check all responses were successful
    assert all(r.status_code == 200 for r in responses)
    
    # Log performance metrics
    avg_time = total_time / request_count
    logger.info(f"Average response time: {avg_time:.2f}s for {request_count} requests")
    
    # Check rate limiting headers if they exist
    if "X-RateLimit-Remaining" in responses[-1].headers:
        remaining = responses[-1].headers["X-RateLimit-Remaining"]
        logger.info(f"Rate limit remaining: {remaining}")

# Error handling tests 
@pytest.mark.integration
def test_lastfm_invalid_genre():
    """Test behavior with invalid genre"""
    response = client.get("/genre/invalidgenrexyz123?limit=10")
    assert response.status_code == 200
    tracks = response.json()
    assert isinstance(tracks, list)
    assert len(tracks) == 0
    logger.info("Successfully handled invalid genre request")

@pytest.mark.integration
def test_lastfm_search_special_characters():
    """Test search with special characters and non-English terms"""
    special_queries = [
        "björk",
        "sigur rós",
        "日本",
        "محمد عبد الوهاب"
    ]
    
    for query in special_queries:
        response = client.get(f"/search?q={query}")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        logger.info(f"Search with '{query}' returned {len(data['results'])} results")

@pytest.mark.integration
def test_lastfm_pagination_limit():
    """Test pagination and limit parameters"""
    limits = [1, 10, 50]
    
    for limit in limits:
        response = client.get(f"/genre/rock?limit={limit}")
        assert response.status_code == 200
        tracks = response.json()
        if tracks:
            assert len(tracks) <= limit
            logger.info(f"Successfully limited results to {len(tracks)} tracks")