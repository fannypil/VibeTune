import httpx
from typing import Dict
from lastfm_client import LastFMClient

class AIAgentClient:
    def __init__(self, base_url: str = "http://ai_agent:8003"):
        self.base_url = base_url

    async def generate(self, prompt: str) -> Dict:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/generate",
                json={"prompt": prompt}
            )
            response.raise_for_status()
            return response.json()
        
class PlaylistGeneratorService:
    def __init__(self, ai_client=None, lastfm_client=None):
        self.ai_client = ai_client or AIAgentClient()
        self.lastfm_client = lastfm_client or LastFMClient()

    async def generate_playlist(self, prompt: str, track_limit: int = 10):
        # 1. Get keywords from AI agent
        ai_result = await self.ai_client.generate(prompt)
        keywords = ai_result.get("keywords", [])
        # 2. Search Last.fm for tracks
        tracks = await self.lastfm_client.search_tracks(keywords, limit=track_limit)
        return {
            "ai_result": ai_result,
            "tracks": tracks
        }