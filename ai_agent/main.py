from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import json
import logging
from typing import List

logger = logging.getLogger(__name__)
app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str


SONG_PROMPT_TEMPLATE = """
You are a music recommendation assistant.

Given a user's request, recommend a list of 8–12 real songs that match the user's mood, vibe, or situation.

Guidelines:
- Songs must be real and released between 1980 and 2025.
- Include a mix of both newer and classic songs.
- Try to suggest both popular hits and lesser-known tracks.
- Do NOT repeat the user's text.
- Return clean JSON array only. Do not include explanations, genres, release dates, or any text outside of the array.

Return your answer strictly in this format:
[
  {{ "title": "Song Title", "artist": "Artist Name" }},
  ...
]
Do not include any explanations, genres, tags, or extra text. Only return the JSON array.
User request: "{user_prompt}"
"""

@app.post("/generate")
async def generate(request: PromptRequest):
    prompt = SONG_PROMPT_TEMPLATE.format(user_prompt=request.prompt)
    try:
        result = subprocess.run(
            ["ollama", "run", "gemma:2b", prompt],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail="LLM generation failed")
        # Try to extract JSON from the output
        output = result.stdout
        logger.error(f"LLM raw output: {output}")  # Add this line
        json_start = output.find('[')
        json_end = output.rfind(']')
        if json_start == -1 or json_end == -1:
            raise HTTPException(status_code=500, detail="No JSON found in LLM output")
        songs = json.loads(output[json_start:json_end+1])
        return songs
    except Exception as e:
        logger.error(f"Error generating songs: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
