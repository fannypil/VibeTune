from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .track import TrackOut

class PlaylistBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_favorite: Optional[bool] = False

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistOut(PlaylistBase):
    id: int
    created_at: datetime
    user_id: int
    tracks: list[TrackOut] = []

    class Config:
        orm_mode = True
