import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def search_youtube_video(query: str) -> Optional[str]:
    if not YOUTUBE_API_KEY:
        raise Exception("Missing YouTube API key")

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "q": query,
        "part": "snippet",
        "maxResults": 1,
        "type": "video",
        "key": YOUTUBE_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 403:
            raise Exception("Invalid API key or quota exceeded")
            
        data = response.json()
        
        if response.status_code != 200:
            error_message = data.get("error", {}).get("message", "Unknown error")
            raise Exception(f"YouTube API error: {error_message}")
            
        items = data.get("items", [])
        if items:
            return items[0]["id"]["videoId"]
        return None
        
    except requests.RequestException as e:
        raise Exception(f"Network error: {str(e)}")