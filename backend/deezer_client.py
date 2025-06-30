import requests

BASEURL="https://api.deezer.com"

import requests

BASEURL = "https://api.deezer.com"

def search_deezer_track_image(query: str) -> str:
    """
    Search for a Deezer track and return the album cover if available,
    otherwise fallback to artist picture.
    """
    try:
        url = f"{BASEURL}/search?q={query}"
        response = requests.get(url)
        data = response.json()
        if not data.get("data"):
            return None

        first_result = data["data"][0]

        # Try getting track album cover first
        if "album" in first_result and "cover_medium" in first_result["album"]:
            return first_result["album"]["cover_medium"]

        # Fallback: get artist picture
        if "artist" in first_result and "picture_medium" in first_result["artist"]:
            return first_result["artist"]["picture_medium"]

        return None
    except Exception:
        return None

def search_deezer_artist_image(artist_name: str) -> str:
    """
    Search for a Deezer artist and return their picture.
    """
    try:
        url = f"{BASEURL}/search/artist?q={artist_name}"
        response = requests.get(url)
        data = response.json()
        if not data.get("data"):
            return None

        first_result = data["data"][0]
        if "picture_medium" in first_result:
            return first_result["picture_medium"]

        return None
    except Exception:
        return None