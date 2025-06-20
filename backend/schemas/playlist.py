from pydantic import BaseModel, Field
from typing import List, Optional
from .track import TrackBase, TrackOut
from datetime import datetime


class PlaylistBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    # is_favorite: bool = False

class PlaylistCreate(PlaylistBase):
    tracks: List[TrackBase] = []

class PlaylistUpdate(PlaylistBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    # is_favorite: Optional[bool] = None
    tracks: Optional[List[TrackBase]] = None

class PlaylistOut(PlaylistBase):
    id: int
    created_at: datetime
    user_id: int
    tracks: List[TrackOut] = []
    is_favorite: Optional[bool] = None  # Only here, set per-request

    class Config:
        # orm_mode = True
        from_attributes = True

class SearchResponse(BaseModel):
    results: List[TrackBase]
    total: Optional[int] = None

class PlaylistPromptRequest(BaseModel):
    prompt: str
