# schemas/artist.py
from pydantic import BaseModel
from typing import Optional


class Artist(BaseModel):
    name: str
    playcount: Optional[int]
    listeners: Optional[int]
    mbid: Optional[str]
    url: Optional[str]
    streamable: Optional[bool]
    image_small: Optional[str]
    image_medium: Optional[str]
    image_large: Optional[str]
    image_extralarge: Optional[str]
    image_mega: Optional[str]
