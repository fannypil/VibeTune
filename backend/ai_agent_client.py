import httpx
from typing import Dict,List
import logging
from schemas.quiz import QuizRequest

logger = logging.getLogger(__name__)

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
        
def build_prompt_from_quiz(data: QuizRequest) -> str:
    genre_text = ", ".join(data.preferred_genres)
    discovery_text = {
        "popular": "well-known and beloved hits",
        "fresh": "lesser-known or recently released songs",
        "mix": "a mix of popular and fresh tracks"
    }.get(data.discovery_mode, "a variety of tracks")
    decade_text = f"songs from the {data.decade}" if data.decade else "songs from all decades"


    prompt = (
        f"I'm feeling {data.mood} and I'm about to {data.activity}. "
        f"I love {genre_text} music, especially {decade_text}. "
        f"Please recommend 10-12 songs that match this vibe, focusing on {discovery_text}. "
        "Only return a JSON array with song title and artist."
    )
    return prompt