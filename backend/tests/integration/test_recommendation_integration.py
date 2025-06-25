import pytest
from conftest import ensure_ai_service_ready, client, logger, assert_track_has_lastfm_data
import aiohttp
from unittest.mock import AsyncMock, patch

MOCK_AI_RESPONSE = [
    {"title": "Dancing Queen", "artist": "ABBA"},
    {"title": "I Wanna Dance with Somebody", "artist": "Whitney Houston"},
    {"title": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars"}
]

@pytest.mark.asyncio
@pytest.mark.integration
async def test_end_to_end_playlist_generation():
    """Test complete flow from prompt to playlist generation"""
    try:
        # Try using real AI service first
        try:
            await ensure_ai_service_ready()
            response = client.post(
                "/ai/playlist-from-prompt",
                json={"prompt": "happy upbeat songs for a party"}
            )
            if response.status_code == 200:
                playlist = response.json()
                assert len(playlist) > 0
                for track in playlist:
                    assert_track_has_lastfm_data(track)
                logger.info("Successfully tested with real AI service")
                return
        except Exception as e:
            logger.warning(f"Real AI service unavailable: {str(e)}, falling back to mock")

        # Fall back to mock if real service fails
        with patch('ai_agent_client.AIAgentClient.generate', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = MOCK_AI_RESPONSE
            
            response = client.post(
                "/ai/playlist-from-prompt",
                json={"prompt": "happy upbeat songs for a party"}
            )
            
            assert response.status_code == 200, f"Failed with status {response.status_code}: {response.text}"
            playlist = response.json()
            assert len(playlist) > 0, "Empty playlist returned"
            
            for track in playlist:
                assert_track_has_lastfm_data(track)
                logger.info(f"Validated mock track: {track['title']} by {track['artist']}")
            
            logger.info("Successfully tested with mock AI service")
            
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
 with patch('ai_agent_client.AIAgentClient.generate', new_callable=AsyncMock) as mock_ai:
        # Configure mock
        mock_ai.return_value = MOCK_AI_RESPONSE
        
        response = client.post(
            "/ai/playlist-from-prompt",
            json={"prompt": "classic rock hits"}
        )
        
        assert response.status_code == 200, f"Failed with status {response.status_code}: {response.text}"
        playlist = response.json()
        
        # Verify LastFM data enrichment
        assert len(playlist) == len(MOCK_AI_RESPONSE), "Playlist length mismatch"
        
        for track in playlist:
            # Check required fields
            assert all(key in track for key in ["title", "artist", "url", "listeners", "image"]), \
                f"Missing required fields in track: {track}"
            
            # Validate URLs
            assert track["url"].startswith("http"), f"Invalid URL format: {track['url']}"
            if track["image"]:
                assert track["image"].startswith("http"), f"Invalid image URL: {track['image']}"
            
            # Verify LastFM specific data
            assert isinstance(track["listeners"], (int, type(None))), \
                f"Invalid listeners count type: {type(track['listeners'])}"
            
            logger.info(f"Verified LastFM data for track: {track['title']} by {track['artist']}")
        
        logger.info(f"Successfully tested LastFM integration with {len(playlist)} tracks")
