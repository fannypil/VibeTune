from pydantic import BaseModel
from typing import Optional

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