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
    keywords: List[str]

SYSTEM_PROMPT = """You are a music recommendation assistant.
Analyze the user's input and provide:
, return only a JSON object with the following structure:
{{
  "genres": [list of music genres],
  "moods": [list of mood adjectives],
  "keywords": [list of relevant keywords]
}}

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