import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def search_youtube_video(query: str) -> Optional[str]:
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "q": query,
        "part": "snippet",
        "maxResults": 1,
        "type": "video",
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        if items:
            return items[0]["id"]["videoId"]
    return None
