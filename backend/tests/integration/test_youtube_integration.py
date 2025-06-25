import pytest
from conftest import client
import logging
from unittest.mock import patch


logger = logging.getLogger(__name__)
TEST_ENDPOINT = "/track/youtube-track"
COMMON_TEST_CASES = {
    "standard": {"title": "Bohemian Rhapsody", "artist": "Queen"},
    "special_chars": [
        {"title": "99 Luftballons", "artist": "Nena"},
        {"title": "Águas de Março", "artist": "Elis Regina"}
    ],
    "structured": [
        {"title": "Stairway to Heaven", "artist": "Led Zeppelin"},
        {"title": "Led Zeppelin - Stairway to Heaven", "artist": ""},
        {"title": "Stairway to Heaven (Live)", "artist": "Led Zeppelin"},
        {"title": "Stairway to Heaven Official Video", "artist": "Led Zeppelin"}
    ]
}

def make_youtube_request(track_title: str, artist: str):
    """Helper function to make YouTube track requests"""
    return client.get(
        TEST_ENDPOINT,
        params={"track_title": track_title, "artist": artist}
    )

def assert_valid_youtube_response(response, expect_video=True):
    """Helper function to validate YouTube API responses"""
    assert response.status_code == 200
    result = response.json()
    
    if expect_video:
        assert "video_id" in result
        assert len(result["video_id"]) > 0
    else:
        assert "error" in result or result.get("video_id") is None
    
    return result

@pytest.mark.integration
def test_youtube_search_integration():
    """Test YouTube video search for tracks"""
    case = COMMON_TEST_CASES["standard"]
    response = make_youtube_request(case["title"], case["artist"])
    assert_valid_youtube_response(response)
    logger.info(f"Successfully found video for '{case['artist']} - {case['title']}'")


@pytest.mark.integration
def test_youtube_search_with_special_characters():
    """Test YouTube search with non-standard characters"""
    for case in COMMON_TEST_CASES["special_chars"]:
        response = make_youtube_request(case["title"], case["artist"])
        assert_valid_youtube_response(response)
        logger.info(f"Successfully found video for '{case['artist']} - {case['title']}'")

@pytest.mark.integration
def test_youtube_invalid_api_key():
    """Test behavior when YouTube API key is invalid"""
    with patch('youtube_client.YOUTUBE_API_KEY', 'invalid_key'):
        response = client.get(
            "/track/youtube-track",
            params={
                "track_title": "Test Song",
                "artist": "Test Artist"
            }
        )
        assert response.status_code == 200  # Our API should still return 200
        result = response.json()
        assert result.get("error") is not None
        logger.info("Successfully handled invalid API key scenario")

@pytest.mark.integration
def test_youtube_long_query():
    """Test behavior with extremely long search queries"""
    response = make_youtube_request("x" * 100, "y" * 100)
    assert_valid_youtube_response(response, expect_video=False)
    logger.info("Successfully handled long query")

@pytest.mark.integration
def test_youtube_rate_limiting():
    """Test handling of YouTube API rate limits"""
    for i in range(5):
        response = make_youtube_request(f"Test Song {i}", "Test Artist")
        assert response.status_code == 200
        if "error" in response.json():
            logger.info("Rate limiting detected as expected")
            return
    logger.warning("No rate limiting encountered during test")

@pytest.mark.integration
def test_youtube_empty_results():
    """Test behavior when no videos are found"""
    response = make_youtube_request("xxxxxxxxxxxxxxxxxxxxxxxxxxx", "yyyyyyyyyyyyyyyyyyyyyyyyyyy")
    assert_valid_youtube_response(response, expect_video=False)
    logger.info("Successfully handled no results case")

@pytest.mark.integration
def test_youtube_structured_search():
    """Test different search query structures"""
    video_ids = set()
    for variant in COMMON_TEST_CASES["structured"]:
        response = make_youtube_request(variant["title"], variant["artist"])
        result = assert_valid_youtube_response(response)
        if "video_id" in result:
            video_ids.add(result["video_id"])
    
    assert len(video_ids) <= 2, "Too much variation in search results"
    logger.info("Successfully tested different search structures")