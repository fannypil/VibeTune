from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import subprocess
import json
import logging

logger = logging.getLogger(__name__)
app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

class MoodAnalysis(BaseModel):
    genres: List[str]
    moods: List[str]
    tags: List[str]

SYSTEM_PROMPT = """
You are a music recommendation assistant.
Given a user's request, return:
- 3-5 music genres that fit the emotional intent (e.g., cheerful, energetic, positive)
- 3-5 mood tags (e.g., happy, dance, party, feelgood, relaxing)
- 3-5 Last.fm tag keywords (not track names) that will help find music with the desired emotional effect

Return only a JSON object with this structure:
{
  "genres": [list of genres],
  "moods": [list of moods],
  "tags": [list of Last.fm tag keywords]
}
User input: {request.prompt}
Only respond with the JSON. No markdown, no explanation.
"""

@app.post("/generate", response_model=MoodAnalysis)
async def generate(request: PromptRequest):
    try:
        result = subprocess.run(
            ["ollama", "run", "gemma:2b", SYSTEM_PROMPT + "\n\nUser input: " + request.prompt],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail="LLM generation failed")
        response = json.loads(result.stdout)
        return MoodAnalysis(**response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}