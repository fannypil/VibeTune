from pydantic import BaseModel
from typing import Optional

class Track(BaseModel):
    name: str
    artist: str
    url: Optional[str] = None