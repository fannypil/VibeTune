import pytest
from conftest import client, ensure_ai_service_ready
import logging
import asyncio
import time

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
@pytest.mark.integration
async def test_complete_user_journey():
    """Test complete user journey from registration to playlist creation"""
    try:
        # Generate unique email and username using timestamp
        timestamp = int(time.time())
        test_email = f"integration{timestamp}@test.com"
        test_username = f"integration_user_{timestamp}"

        # 1. Register user
        register_response = client.post(
            "/auth/register",
            json={
                "username": "integration_test_user",
                "email": "integration@test.com",
                "password": "TestPass123",
                "first_name": "Test",
                "last_name": "User"
            }
        )
        assert register_response.status_code == 200
        logger.info("User registration successful")

        # 2. Login
        login_response = client.post(
            "/auth/login",
            data={
                "username": "integration@test.com",
                "password": "TestPass123"
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Generate AI playlist
        max_retries = 3
        for attempt in range(max_retries):
            try:
                await ensure_ai_service_ready()
                playlist_response = client.post(
                    "/ai/playlist-from-prompt",
                    json={"prompt": "happy rock songs"},
                    headers=headers
                )
                
                if playlist_response.status_code == 200:
                    tracks = playlist_response.json()
                    logger.info(f"Generated playlist with {len(tracks)} tracks")
                    break
                else:
                    error_detail = playlist_response.json().get('detail', 'No error detail')
                    logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {error_detail}")
                    if attempt == max_retries - 1:
                        pytest.fail(f"Failed to generate playlist after {max_retries} attempts")
                    await asyncio.sleep(3)
                    
            except Exception as e:
                logger.error(f"Attempt {attempt + 1}/{max_retries} failed with error: {str(e)}")
                if attempt == max_retries - 1:
                    raise


        # 4. Create playlist
        create_playlist_response = client.post(
            "/playlist/",
            json={
                "name": "My AI Generated Playlist",
                "description": "Generated from integration test"
            },
            headers=headers
        )
        assert create_playlist_response.status_code == 200
        playlist_id = create_playlist_response.json()["id"]

        # 5. Add tracks to playlist
        for track in tracks[:3]:  # Add first 3 tracks
            track_data = {
                "name": track["title"],
                "artist": track["artist"],
                "url": track.get("url", f"https://example.com/{track['artist']}/{track['title']}"),
                "image_url": track.get("image", "https://example.com/default.jpg"),
                "playlist_id": playlist_id
            }
            
            try:
                add_track_response = client.post(
                    f"/track/{playlist_id}/tracks",  # Updated endpoint path
                    json=track_data,
                    headers=headers
                )
                
                if add_track_response.status_code != 200:
                    error_detail = add_track_response.json()
                    logger.error(f"Failed to add track: {error_detail}")
                    
                assert add_track_response.status_code == 200, \
                    f"Failed to add track: {add_track_response.text}"
                    
                logger.info(f"Successfully added track: {track['title']}")
                
            except Exception as e:
                logger.error(f"Error adding track {track['title']}: {str(e)}")
                logger.error(f"Track data: {track_data}")
                raise

        # 6. Verify final playlist
        final_playlist = client.get(f"/playlist/{playlist_id}", headers=headers)
        assert final_playlist.status_code == 200
        assert len(final_playlist.json()["tracks"]) == 3
        logger.info("Successfully verified final playlist")
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise



        
