from pydantic import BaseModel
from typing import Optional

class Artist(BaseModel):
    name: str
    playcount: Optional[int]
    listeners: Optional[int]
    mbid: Optional[str]
    url: Optional[str]
    streamable: Optional[bool]
    image: Optional[str]
