from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from .track import TrackBase, TrackOut
from datetime import datetime


class PlaylistBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class PlaylistCreate(PlaylistBase):
    tracks: List[TrackBase] = []

class PlaylistUpdate(PlaylistBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    tracks: Optional[List[TrackBase]] = None

class PlaylistOut(PlaylistBase):
    id: int
    created_at: datetime
    user_id: int
    tracks: List[TrackOut] = []
    is_favorite: Optional[bool] = None  # Only here, set per-request

    model_config = ConfigDict(from_attributes=True)  # Replace Config class

class SearchResponse(BaseModel):
    results: List[TrackBase]
    error: Optional[str] = None

class PlaylistPromptRequest(BaseModel):
    prompt: str

class PlaylistSummary(PlaylistBase):
    id: int
    created_at: datetime
    is_favorite: Optional[bool] = None  # Only here, set per-request

    class Config:
        from_attributes = True
