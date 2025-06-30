from typing import List
from schemas import Track
from schemas.track import LLMResponseItem  
from lastfm_client import LastFMClient
from youtube_client import search_youtube_video

class PlaylistService:
    def __init__(self):
        self.lastfm = LastFMClient()

    async def generate_playlist_from_llm_response(self, songs: List[LLMResponseItem]) -> List[Track]:
        playlist = []
        for song in songs:
            track = await self.lastfm.search_tracks(song.title.strip(), song.artist.strip())
            if track:
                playlist.append(track)
        return playlist