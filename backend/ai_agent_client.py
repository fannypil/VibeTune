import httpx
from typing import Dict

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