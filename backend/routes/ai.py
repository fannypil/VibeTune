from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List
import logging
from schemas import Track, QuizRequest
from ai_agent_client import AIAgentClient, build_prompt_from_quiz
from playlist_manager import PlaylistService
from schemas.track import LLMResponseItem

logger = logging.getLogger(__name__)
router = APIRouter()
ai_agent = AIAgentClient()
playlist_service = PlaylistService()



class PromptRequest(BaseModel):
    prompt: str

@router.post("/playlist-from-prompt", response_model=List[Track])
async def playlist_from_prompt(request: PromptRequest):
    try:
        # 1. Get songs from LLM
        songs = await ai_agent.generate(request.prompt)
        # songs is a list of dicts: [{ "title": ..., "artist": ... }, ...]
        # 2. Convert to LLMResponseItem list
        llm_songs = [LLMResponseItem(**song) for song in songs]
        # 3. Search Last.fm for each song
        playlist = await playlist_service.generate_playlist_from_llm_response(llm_songs)
        if not playlist:
            raise HTTPException(status_code=404, detail="No valid tracks found")
        return playlist
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI service error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )

@router.post("/playlist-from-quiz", response_model=List[Track])
async def playlist_from_quiz(request: QuizRequest):
    user_prompt = build_prompt_from_quiz(request)
    songs = await ai_agent.generate(user_prompt)
    llm_songs = [LLMResponseItem(**song) for song in songs]
    playlist = await playlist_service.generate_playlist_from_llm_response(llm_songs)
    if not playlist:
        raise HTTPException(status_code=404, detail="No valid tracks found")
    return playlist
