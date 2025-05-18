from pydantic import BaseModel
from typing import List
from .track import Track

class PlaylistResponse(BaseModel):
    playlist: List[Track]

    
class SearchResponse(BaseModel):
    results: List[Track]