from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import json
import os
import google.generativeai as genai
from typing import List, Dict

# --- Basic Configuration ---
app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Gemini API Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    logger.warning("GEMINI_API_KEY not found. The /generate endpoint will not work.")

class PromptRequest(BaseModel):
    prompt: str

# SONG_PROMPT_TEMPLATE = """
# You are a music recommendation assistant.

# Given a user's request, recommend a list of 8–12 real songs that match the user's mood, vibe, or situation.

# Guidelines:
# - Songs must be real and released between 1980 and 2025.
# - Include a mix of both newer and classic songs.
# - Try to suggest both popular hits and lesser-known tracks.
# - Do NOT repeat the user's text.
# - Return clean JSON array only. Do not include explanations, genres, release dates, or any text outside of the array.

# Return your answer strictly in this format:
# [
#   {{ "title": "Song Title", "artist": "Artist Name" }},
#   ...
# ]
# Do not include any explanations, genres, tags, or extra text. Only return the JSON array.
# User request: "{user_prompt}"
# """
SYSTEM_PROMPT = """
You are VibeTune, a world-class music recommendation AI.
Your goal is to create a perfect playlist of 8 to 12 songs based on a user's request.

Follow these rules strictly:
1.  **Real Songs Only:** All recommendations must be real, officially released songs.
2.  **Variety is Key:** Include a mix of well-known hits and lesser-known gems that fit the vibe.
3.  **Timeframe:** Prioritize songs released between 1980 and 2025, unless the user specifies otherwise.
4.  **No Repeats:** Do not repeat songs in the list.
5.  **JSON Output Only:** Your entire response must be a single, valid JSON array of objects. Each object must contain two keys: "title" and "artist". Do not include any other text, explanations, or markdown formatting.
6. Return your answer strictly in this format:
[
  {{ "title": "Song Title", "artist": "Artist Name" }},
  ...
]
"""

@app.post("/generate", response_model=List[Dict])
async def generate(request: PromptRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API key is not configured on the server.")

    # Use gemini-1.5-flash and enable JSON mode for reliable, structured output
    model = genai.GenerativeModel(
        'gemini-1.5-flash-latest',
        system_instruction=SYSTEM_PROMPT,
        generation_config=genai.types.GenerationConfig(
            # This forces the model to output valid JSON
            response_mime_type="application/json"
        )
    )

    # The user prompt is now simpler, as most instructions are in the system prompt
    user_prompt = f"Create a playlist for the following request: \"{request.prompt}\""

    try:
        response = await model.generate_content_async(user_prompt)
        
        # With JSON mode, the response text is clean JSON, so we can parse it directly.
        # No more manual string cleaning is needed!
        songs = json.loads(response.text)
        return songs

    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON from Gemini response. Response: {response.text}")
        raise HTTPException(status_code=500, detail="Failed to parse AI response.")
    except Exception as e:
        logger.error(f"An error occurred with the Gemini API: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred with the AI service: {str(e)}")

@app.get("/health")
async def health_check():
    """Checks if the service is running and the API key is present."""
    if not GEMINI_API_KEY:
        return {"status": "unhealthy", "reason": "GEMINI_API_KEY is not set"}