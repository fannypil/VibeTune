from pydantic import BaseModel
from typing import List

class QuizRequest(BaseModel):
    mood: str
    activity: str
    preferred_genres: List[str]
    decade: str
    discovery_mode : str
