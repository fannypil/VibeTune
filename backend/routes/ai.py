from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from schemas import Track
from ai_agent_client import AIAgentClient
from playlist_manager import PlaylistService

router = APIRouter()
ai_agent = AIAgentClient()
playlist_service = PlaylistService()



class PromptRequest(BaseModel):
    prompt: str

@router.post("/playlist-from-prompt", response_model=List[Track])
async def playlist_from_prompt(request: PromptRequest):
    # 1. Get songs from LLM
    songs = await ai_agent.generate(request.prompt)
    # songs is a list of dicts: [{ "title": ..., "artist": ... }, ...]
    # 2. Convert to LLMResponseItem list
    from schemas.track import LLMResponseItem
    llm_songs = [LLMResponseItem(**song) for song in songs]
    # 3. Search Last.fm for each song
    playlist = await playlist_service.generate_playlist_from_llm_response(llm_songs)
    if not playlist:
        raise HTTPException(status_code=404, detail="No valid tracks found")
    return playlist