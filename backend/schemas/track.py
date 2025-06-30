from pydantic import BaseModel
from typing import Optional, List

class TrackBase(BaseModel):
    name: str
    artist: str
    url: Optional[str] = None

class TrackCreate(TrackBase):
    playlist_id: int

class TrackOut(TrackBase):
    id: int
    playlist_id: int

    class Config:
        # orm_mode = True
        from_attributes = True
        
class Track(BaseModel):
    title: str
    artist: str
    # videoId: str
    image: Optional[str] = None

class LLMResponseItem(BaseModel):
    title: str
    artist: str

class LLMResponse(BaseModel):
    songs: List[LLMResponseItem]


