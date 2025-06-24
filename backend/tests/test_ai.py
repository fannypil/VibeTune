from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@patch("ai_agent_client.AIAgentClient.generate", new_callable=AsyncMock)
@patch("playlist_manager.PlaylistService.generate_playlist_from_llm_response", new_callable=AsyncMock)
def test_playlist_from_prompt_success(mock_generate_playlist, mock_generate_ai):
    # Mock AI agent response
    mock_generate_ai.return_value = [
        {
            "title": "Imagine",
            "artist": "John Lennon"
        }
    ]

    # Mock playlist service response matching Track schema
    mock_generate_playlist.return_value = [
        {
            "title": "Imagine",
            "artist": "John Lennon",
            "url": "http://example.com",
            "listeners": 1000000,
            "image": "http://example.com/image.jpg"  # Changed to string as per schema
        }
    ]

    response = client.post("/ai/playlist-from-prompt", json={"prompt": "calm music"})
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Imagine"
    assert response.json()[0]["artist"] == "John Lennon"
    assert response.json()[0]["url"] == "http://example.com"
    assert response.json()[0]["image"] == "http://example.com/image.jpg"
    
    # Verify mocks were called correctly
    mock_generate_ai.assert_called_once_with("calm music")
    mock_generate_playlist.assert_called_once()

@patch("ai_agent_client.AIAgentClient.generate", new_callable=AsyncMock)
@patch("playlist_manager.PlaylistService.generate_playlist_from_llm_response", new_callable=AsyncMock)
def test_playlist_from_quiz_success(mock_generate_playlist, mock_generate_ai):
    # Mock AI agent response
    mock_generate_ai.return_value = [
        {
            "title": "Dancing Queen",
            "artist": "ABBA"
        }
    ]
    
    mock_generate_playlist.return_value = [
        {
            "title": "Dancing Queen",
            "artist": "ABBA",
            "url": "http://example.com",
            "listeners": 2000000,
            "image": "http://example.com/abba.jpg"
        }
    ]

    quiz_data = {
        "mood": "happy",
        "activity": "dancing",
        "preferred_genres": ["pop", "disco"],
        "decade": "90s",
        "discovery_mode": "fresh",
    }
    response = client.post("/ai/playlist-from-quiz", json=quiz_data)
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Dancing Queen"
    assert response.json()[0]["artist"] == "ABBA"

def test_empty_playlist_response(client, test_db):
    with patch("ai_agent_client.AIAgentClient.generate", new_callable=AsyncMock) as mock_ai, \
         patch("playlist_manager.PlaylistService.generate_playlist_from_llm_response", new_callable=AsyncMock) as mock_playlist:
        
        mock_ai.return_value = [{"title": "Unknown Song", "artist": "Unknown Artist"}]
        mock_playlist.return_value = []  # Empty playlist
        
        response = client.post("/ai/playlist-from-prompt", json={"prompt": "some music"})
        assert response.status_code == 404
        assert response.json()["detail"] == "No valid tracks found"

def test_invalid_quiz_data(client, test_db):
    invalid_quiz = {
        "mood": "",  # Empty mood
        "genre": "pop",
        "era": "invalid_era",  # Invalid era
        "occasion": "party"
    }
    
    response = client.post("/ai/playlist-from-quiz", json=invalid_quiz)
    assert response.status_code == 422  # Validation error
    
def test_ai_service_error(client, test_db):
    with patch("ai_agent_client.AIAgentClient.generate", new_callable=AsyncMock) as mock_ai:
        mock_ai.side_effect = Exception("AI service unavailable")
        
        response = client.post("/ai/playlist-from-prompt", json={"prompt": "some music"})
        assert response.status_code == 500
        assert "error" in response.json()["detail"].lower()