from pydantic import BaseModel, Field
from typing import List, Optional
from .track import Track
from datetime import datetime

class PlaylistBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class PlaylistCreate(PlaylistBase):
    tracks: List[Track] = []

class PlaylistUpdate(PlaylistBase):
    tracks: Optional[List[Track]] = None

class PlaylistResponse(PlaylistBase):
    id: str
    tracks: List[Track] 
    user_id: str
    
class SearchResponse(BaseModel):
    results: List[Track]
    total: Optional[int] = None