from fastapi import APIRouter, Query
from lastfm_client import get_lastfm_top_tracks, search_lastfm_tracks, get_lastfm_top_artists
from schemas import TrackBase, SearchResponse, Artist
from typing import List

router = APIRouter()


# dummy endpoint to simulate a playlist
# This should be removed
@router.get("/playlist")
async def get_playlist():
    playlist = [
        {"title": "Song A", "artist": "Artist 1"},
        {"title": "Song B", "artist": "Artist 2"},
        {"title": "Song C", "artist": "Artist 3"},
    ]
    return playlist

@router.get("/lastfm-top-tracks", response_model=SearchResponse)
async def lastfm_top_tracks():
    try:
        tracks = get_lastfm_top_tracks()
        simplified_tracks = [
            TrackBase(
                name=track.get("name"),
                artist=track.get("artist", {}).get("name"),
                url=track.get("url")
            )
            for track in tracks
        ]
        return {"results": simplified_tracks}
    except Exception as e:
        return {"error": str(e)}

@router.get("/search", response_model=SearchResponse)
async def search_tracks(q: str = Query(..., description="Song name or artist to search")):
    try:
        tracks = search_lastfm_tracks(q)
        simplified_tracks = [
            TrackBase(
                name=track.get("name"),
                artist=track.get("artist"),
                url=track.get("url")
            )
            for track in tracks
        ]
        return {"results": simplified_tracks}
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/lastfm-top-artists", response_model=List[Artist])
async def lastfm_top_artists():
    try:
        artists_raw = get_lastfm_top_artists()
        artists = []

        for artist in artists_raw:
            images = {img["size"]: img["#text"] for img in artist.get("image", [])}
            artists.append(Artist(
                name=artist.get("name"),
                playcount=int(artist.get("playcount", 0)),
                listeners=int(artist.get("listeners", 0)),
                mbid=artist.get("mbid"),
                url=artist.get("url"),
                streamable=artist.get("streamable") == "1",
                image_small=images.get("small"),
                image_medium=images.get("medium"),
                image_large=images.get("large"),
                image_extralarge=images.get("extralarge"),
                image_mega=images.get("mega")
            ))

        return artists

    except Exception as e:
        return {"error": str(e)}