from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

class TrackSuggestion(BaseModel):
    title: str
    artist: str

@app.post("/generate")
def generate_playlist(req: PromptRequest) -> List[TrackSuggestion]:
    # Placeholder AI response
    return [
        {"title": "Fix You", "artist": "Coldplay"},
        {"title": "Someone Like You", "artist": "Adele"}
    ]
