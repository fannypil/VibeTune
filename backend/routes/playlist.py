from fastapi import APIRouter, HTTPException, Depends
from models import PlaylistResponse, PlaylistCreate, PlaylistUpdate, Track
from .auth import get_current_user

router = APIRouter(prefix="/playlist", tags=["Playlists"])

# Dummy data
DUMMY_PLAYLIST = {
    "id": "playlist_1",
    "name": "My Playlist",
    "description": "A dummy playlist",
    "tracks": [
        {"name": "Song 1", "artist": "Artist 1"},
        {"name": "Song 2", "artist": "Artist 2"}
    ],
    "user_id": "dummy_user_id"
}

@router.post("/", response_model=PlaylistResponse)
async def create_playlist(
    playlist: PlaylistCreate,
    current_user = Depends(get_current_user)
):
    """Create a dummy playlist"""
    return DUMMY_PLAYLIST

@router.get("/{playlist_id}", response_model=PlaylistResponse)
async def get_playlist(playlist_id: str):
    """Get a dummy playlist"""
    return DUMMY_PLAYLIST

@router.put("/{playlist_id}", response_model=PlaylistResponse)
async def update_playlist(
    playlist_id: str,
    playlist_update: PlaylistUpdate,
    current_user = Depends(get_current_user)
):
    """Update a dummy playlist"""
    return DUMMY_PLAYLIST

@router.delete("/{playlist_id}")
async def delete_playlist(
    playlist_id: str,
    current_user = Depends(get_current_user)
):
    """Delete a dummy playlist"""
    return {"message": "Playlist deleted successfully"}

@router.post("/{playlist_id}/like")
async def like_playlist(
    playlist_id: str,
    current_user = Depends(get_current_user)
):
    """Like a dummy playlist"""
    return {"message": "Playlist added to favorites"}