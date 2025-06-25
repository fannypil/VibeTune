import pytest
from conftest import ensure_ai_service_ready, client, logger, assert_track_has_lastfm_data
import aiohttp

@pytest.mark.asyncio
@pytest.mark.integration
async def test_end_to_end_playlist_generation():
    """Test complete flow from prompt to playlist generation"""
    # Ensure AI service is ready with extended retries
    await ensure_ai_service_ready()
    
    # Check AI service health explicitly
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("http://ai_agent:8003/health") as health_response:
                assert health_response.status == 200, "AI service health check failed"
                health_data = await health_response.json()
                logger.info(f"AI service health status: {health_data}")
        except Exception as e:
            pytest.fail(f"AI service health check failed: {str(e)}")

    # Test the playlist generation
    try:
        response = client.post(
            "/ai/playlist-from-prompt",
            json={"prompt": "happy upbeat songs for a party"}
        )
        
        # If we get a 500, log more details
        if response.status_code == 500:
            error_detail = response.json().get('detail', 'No error detail provided')
            logger.error(f"Playlist generation failed with: {error_detail}")
            
        assert response.status_code == 200, f"Failed with status {response.status_code}: {response.text}"
        
        playlist = response.json()
        assert len(playlist) > 0, "Empty playlist returned"
        
        # Verify track data
        for track in playlist:
            assert_track_has_lastfm_data(track)
            logger.info(f"Validated track: {track['title']} by {track['artist']}")
            
    except Exception as e:
        logger.error(f"Test failed with exception: {str(e)}")
        raise

@pytest.mark.asyncio
@pytest.mark.integration
async def test_quiz_to_playlist_flow():
    """Test playlist generation from quiz answers"""
    await ensure_ai_service_ready()
    
    quiz_data = {
        "mood": "energetic",
        "activity": "workout",
        "preferred_genres": ["rock", "metal"],
        "decade": "2000s",
        "discovery_mode": "mix"
    }
    
    response = client.post("/ai/playlist-from-quiz", json=quiz_data)
    assert response.status_code == 200
    playlist = response.json()
    
    track_stats = {
        "total": len(playlist),
        "popular": 0,
        "fresh": 0
    }
    
    for track in playlist:
        assert_track_has_lastfm_data(track)
        if track["listeners"] > 1000:
            track_stats["popular"] += 1
        else:
            track_stats["fresh"] += 1
    
    assert track_stats["total"] >= 3, "Playlist too short"
    logger.info(f"Playlist stats: {track_stats}")
    
@pytest.mark.asyncio
@pytest.mark.integration
async def test_ai_service_availability():
    """Test AI service health check"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("http://ai_agent:8003/health") as response:
                assert response.status == 200
                data = await response.json()
                assert data["status"] == "healthy"
        except aiohttp.ClientError:
            pytest.fail("AI service is not available")

@pytest.mark.asyncio
@pytest.mark.integration
async def test_lastfm_integration():
    """Test LastFM service integration"""
    response = client.post(
        "/ai/playlist-from-prompt",
        json={"prompt": "classic rock hits"}
    )
    
    assert response.status_code == 200
    playlist = response.json()
    
    # Verify LastFM data enrichment
    for track in playlist:
        assert all(key in track for key in ["title", "artist", "url", "listeners", "image"])
        assert track["url"].startswith("http")
        if track["image"]:
            assert track["image"].startswith("http")

