import os
import requests
import httpx
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
BASE_URL = "http://ws.audioscrobbler.com/2.0/"


def get_lastfm_top_tracks(limit=5):
    api_key = os.getenv("LASTFM_API_KEY")
    if not api_key:
        raise Exception("Missing LASTFM_API_KEY environment variable")

    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "chart.gettoptracks",
        "api_key": api_key,
        "format": "json",
        "limit": limit
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from Last.fm: {response.text}")

    data = response.json()
    return data.get("tracks", {}).get("track", [])

def search_lastfm_tracks(query: str, limit: int = 10):
    api_key = os.getenv("LASTFM_API_KEY")
    url = f"http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.search",
        "track": query,
        "api_key": api_key,
        "format": "json",
        "limit": limit
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        tracks = data.get("results", {}).get("trackmatches", {}).get("track", [])
        return tracks
    else:
        raise Exception(f"Failed to search tracks on Last.fm: {response.text}")

# def generate_youtube_search_url(artist, title):
#     query = f"{artist} {title}".replace(" ", "+")
#     return f"https://www.youtube.com/results?search_query={query}"

class LastFMClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or LASTFM_API_KEY
        self.base_url = BASE_URL
        if not self.api_key:
            raise Exception("Missing LASTFM_API_KEY environment variable")

    async def search_tracks(self, keywords: List[str], limit: int = 10) -> List[Dict]:
        query = " ".join(keywords)
        params = {
            "method": "track.search",
            "track": query,
            "api_key": self.api_key,
            "format": "json",
            "limit": limit
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("results", {}).get("trackmatches", {}).get("track", [])