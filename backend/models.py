from pydantic import BaseModel
from typing import List, Optional

class Track(BaseModel):
    name: str
    artist: str
    url: Optional[str] = None
    # youtube_url: Optional[str] = None

class PlaylistResponse(BaseModel):
    playlist: List[Track]

class SearchResponse(BaseModel):
    results: List[Track]