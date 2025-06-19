from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ai_agent_client import AIAgentClient

router = APIRouter()
ai_client = AIAgentClient()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/generate")
async def generate_playlist_ai(request: PromptRequest):
    try:
        result = await ai_client.generate(request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))