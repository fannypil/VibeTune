from typing import Dict, List, Optional
from models import Track, PlaylistCreate, PlaylistResponse, PlaylistUpdate
from fastapi import HTTPException


class PlaylistManager:
    def __init__(self):
        # In-memory storage (will be replaced with DB later)
        self.playlists: Dict[str, dict] = {}
        self.user_favorites: Dict[str, List[str]] = {}

    async def create_playlist(self, playlist_data: PlaylistCreate, user_id: str) -> PlaylistResponse:
        playlist_id = f"playlist_{len(self.playlists) + 1}"  # Temporary ID generation
        playlist = {
            "id": playlist_id,
            "name": playlist_data.name,
            "tracks": playlist_data.tracks,
            "user_id": user_id
        }
        self.playlists[playlist_id] = playlist
        return PlaylistResponse(**playlist)

    async def get_playlist(self, playlist_id: str) -> Optional[PlaylistResponse]:
        if playlist_id not in self.playlists:
            return None
        return PlaylistResponse(**self.playlists[playlist_id])

    async def update_playlist(
        self, 
        playlist_id: str, 
        playlist_update: PlaylistUpdate, 
        user_id: str
    ) -> Optional[PlaylistResponse]:
        if playlist_id not in self.playlists:
            return None
        
        playlist = self.playlists[playlist_id]
        if playlist["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this playlist")

        playlist.update({
            "name": playlist_update.name,
            "tracks": playlist_update.tracks or playlist["tracks"]
        })
        return PlaylistResponse(**playlist)

    async def like_playlist(self, playlist_id: str, user_id: str) -> bool:
        if playlist_id not in self.playlists:
            return False
        
        if user_id not in self.user_favorites:
            self.user_favorites[user_id] = []
        
        if playlist_id not in self.user_favorites[user_id]:
            self.user_favorites[user_id].append(playlist_id)
        return True

    async def get_user_playlists(self, user_id: str) -> List[PlaylistResponse]:
        return [
            PlaylistResponse(**playlist)
            for playlist in self.playlists.values()
            if playlist["user_id"] == user_id
        ]

    async def get_user_favorites(self, user_id: str) -> List[PlaylistResponse]:
        if user_id not in self.user_favorites:
            return []
        return [
            PlaylistResponse(**self.playlists[playlist_id])
            for playlist_id in self.user_favorites[user_id]
            if playlist_id in self.playlists
        ]