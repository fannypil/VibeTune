from fastapi import APIRouter, HTTPException, Query
from typing import List
from models import Track, PlaylistResponse
from playlist_manager import save_playlist_for_user, get_playlist_for_user

router = APIRouter()

# Simulate user sessions with in-memory storage
@router.post("/playlist/save")
async def save_playlist(user_id: str = Query(...), playlist: List[Track] = []):
    if not playlist:
        raise HTTPException(status_code=400, detail="Playlist is empty")
    save_playlist_for_user(user_id, playlist)
    return {"message": "Playlist saved successfully"}

# Function to retrieve a user's playlist
@router.get("/playlist/user")
async def get_user_playlist(user_id: str = Query(...)) -> PlaylistResponse:
    playlist = get_playlist_for_user(user_id)
    return PlaylistResponse(playlist=playlist)
