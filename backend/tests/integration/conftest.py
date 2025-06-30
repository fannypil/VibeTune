import pytest
import os
import asyncio
import aiohttp
from dotenv import load_dotenv
import pytest_asyncio
import logging
from fastapi.testclient import TestClient
from main import app

load_dotenv()
logger = logging.getLogger(__name__)
client = TestClient(app)

# Configure pytest markers
def pytest_configure(config):
    """Add custom markers to pytest configuration"""
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "asyncio: mark test as async")

@pytest_asyncio.fixture(scope="session")
async def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def http_session():
    """Create aiohttp session for tests."""
    async with aiohttp.ClientSession() as session:
        yield session

@pytest.fixture(autouse=True)
def setup_asyncio_event_loop():
    """Auto-use fixture to set event loop policy"""
    if os.name == 'posix':
        policy = asyncio.get_event_loop_policy()
        loop = policy.new_event_loop()
        asyncio.set_event_loop(loop)
        yield loop
        loop.close()

async def ensure_ai_service_ready():
    """Helper function to ensure AI service is ready"""
    retries = 5  # Increased retries
    retry_delay = 3  # Seconds between retries
    
    for i in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://ai_agent:8003/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"AI service is ready: {data}")
                        return
        except aiohttp.ClientError as e:
            logger.warning(f"AI service not ready (attempt {i+1}/{retries}): {str(e)}")
            if i == retries - 1:
                pytest.fail(f"AI service is not available after {retries} retries")
            await asyncio.sleep(retry_delay)

def assert_track_has_lastfm_data(track):
    """Helper function to verify LastFM track data"""
    required_fields = ["title", "artist"]
    assert all(key in track for key in required_fields), f"Missing required fields in track: {track}"
     # Optional fields
    if "url" in track and track["url"]:
        assert track["url"].startswith("http"), f"Invalid URL format: {track['url']}"
    if "listeners" in track and track["listeners"] is not None:
        assert isinstance(track["listeners"], int), f"Invalid listeners count type: {type(track['listeners'])}"
    if "image" in track and track["image"]:
        assert track["image"].startswith("http"), f"Invalid image URL: {track['image']}"