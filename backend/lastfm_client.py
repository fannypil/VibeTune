import os
import requests
from typing import Optional
from dotenv import load_dotenv
from schemas.track import Track
import random

load_dotenv()

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
BASE_URL = "http://ws.audioscrobbler.com/2.0/"


def get_lastfm_top_tracks(limit=15):
    api_key = LASTFM_API_KEY
    if not api_key:
        raise Exception("Missing LASTFM_API_KEY environment variable")

    # url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "chart.gettoptracks",
        "api_key": api_key,
        "format": "json",
        "limit": limit
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from Last.fm: {response.text}")

    data = response.json()
    return data.get("tracks", {}).get("track", [])

def get_lastfm_top_artists(limit=10):
    api_key = LASTFM_API_KEY
    if not api_key:
        raise Exception("Missing LASTFM_API_KEY environment variable")

    # url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "chart.gettopartists",
        "api_key": api_key,
        "format": "json",
        "limit": limit
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from Last.fm: {response.text}")

    data = response.json()
    return data.get("artists", {}).get("artist", [])

def search_lastfm_tracks(query: str, limit: int = 10):
    api_key = LASTFM_API_KEY
    # url = f"http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.search",
        "track": query,
        "api_key": api_key,
        "format": "json",
        "limit": limit
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        tracks = data.get("results", {}).get("trackmatches", {}).get("track", [])
        return tracks
    else:
        raise Exception(f"Failed to search tracks on Last.fm: {response.text}")
    
def get_tracks_by_tags(tag: str, limit: int = 20, page: int = None):
    if not page:
        page = random.randint(1, 5)
    
    params = {
        "method": "tag.getTopTracks",
        "tag": tag,
        "limit": limit,
        "page": page,
        "api_key": LASTFM_API_KEY,
        "format": "json"
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching genre tracks: {response.text}")
    
    data = response.json()
    return data.get("tracks", {}).get("track", [])
    
    
class LastFMClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or LASTFM_API_KEY
        self.base_url = BASE_URL
        if not self.api_key:
            raise Exception("Missing LASTFM_API_KEY environment variable")

    async def search_tracks(self, title: str, artist: str) -> Optional[Track]:
        params = {
            "method": "track.search",
            "track": title,
            "artist": artist,
            "api_key": self.api_key,
            "format": "json",
            "limit": 1,
        }
        response = requests.get(self.base_url, params=params)  # <-- FIXED HERE
        data = response.json()
        try:
            track_data = data["results"]["trackmatches"]["track"][0]
            return Track(
                title=track_data["name"],
                artist=track_data["artist"],
                url=track_data.get("url"),
                listeners=int(track_data.get("listeners", 0)),
                image=track_data["image"][-1]["#text"] if track_data.get("image") else None
            )
        except (IndexError, KeyError):
            return None