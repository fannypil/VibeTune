from fastapi import APIRouter, Query
from lastfm_client import get_lastfm_top_tracks, search_lastfm_tracks, get_lastfm_top_artists, get_tracks_by_tags
from schemas import TrackBase, SearchResponse, Artist, Track
from typing import List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


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
        return {"results": [], "error": str(e)}

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
    
@router.get("/genre/{tag_name}", response_model=List[Track])
async def get_tracks_for_genre(tag_name: str, limit: int = Query(20, le=50)):
    try:
        raw_tracks = get_tracks_by_tags(tag_name, limit)
        tracks = [
            Track(
                title=t["name"],
                artist=t["artist"]["name"],
                url=t.get("url"),
                image=t["image"][-1]["#text"] if t.get("image") else None,
                # listeners=None
            )
            for t in raw_tracks
        ]
        return tracks[:limit]
    except Exception as e:
        logger.warning(f"Error getting tracks for genre {tag_name}: {str(e)}")
        return []