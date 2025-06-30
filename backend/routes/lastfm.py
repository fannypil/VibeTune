from fastapi import APIRouter, Query
from lastfm_client import get_lastfm_top_tracks, search_lastfm_tracks, get_lastfm_top_artists, get_tracks_by_tags
from schemas import TrackBase, SearchResponse, Artist, Track
from deezer_client import search_deezer_track_image, search_deezer_artist_image
from typing import List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/lastfm-top-tracks", response_model=SearchResponse)
async def lastfm_top_tracks():
    try:
        tracks = get_lastfm_top_tracks()
        # simplified_tracks = [
        #     TrackBase(
        #         name=track.get("name"),
        #         artist=track.get("artist", {}).get("name"),
        #         url=track.get("url")
        #     )
        #     for track in tracks
        # ]
        simplified_tracks = []
        for track in tracks:
            # video_id = await search_youtube_video(track.get("name"), track.get("artist"))
            image = search_deezer_track_image(f"{track.get('name')} {track.get('artist', {}).get('name')}")
            simplified_tracks.append(
                Track(
                    title=track.get("name"),
                    artist=track.get("artist", {}).get("name"),
                    # videoId=video_id,
                    image=image,
                )
            )
        return {"results": simplified_tracks}
    except Exception as e:
        return {"results": [], "error": str(e)}

@router.get("/search", response_model=SearchResponse)
async def search_tracks(q: str = Query(..., description="Song name or artist to search")):
    try:
        tracks = search_lastfm_tracks(q)
        # simplified_tracks = [
        #     TrackBase(
        #         name=track.get("name"),
        #         artist=track.get("artist"),
        #         url=track.get("url")
        #     )
        #     for track in tracks
        # ]
        simplified_tracks = []
        for track in tracks:
            if not isinstance(track, dict):
                continue  # skip invalid entries
            artist = track.get("artist") or "Unknown Artist"
            name = track.get("name") or "Unknown Title"
            image = search_deezer_track_image(f"{name} {artist}")
            simplified_tracks.append(
                Track(
                    title=name,
                    artist=artist,
                    image=image,
                )
            )
        return {"results": simplified_tracks}
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/lastfm-top-artists", response_model=List[Artist])
async def lastfm_top_artists():
    try:
        artists_raw = get_lastfm_top_artists()
        artists = []
        for artist in artists_raw:
            deezer_image = search_deezer_artist_image(artist.get("name") or "")
            artists.append(Artist(
                name=artist.get("name"),
                playcount=int(artist.get("playcount", 0)),
                listeners=int(artist.get("listeners", 0)),
                mbid=artist.get("mbid"),
                url=artist.get("url"),
                streamable=artist.get("streamable") == "1",
                image=deezer_image 
            ))
        return artists
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/genre/{tag_name}", response_model=List[Track])
async def get_tracks_for_genre(tag_name: str, limit: int = Query(20, le=50)):
    try:
        raw_tracks = get_tracks_by_tags(tag_name, limit)
        # tracks = [
        #     Track(
        #         title=t["name"],
        #         artist=t["artist"]["name"],
        #         url=t.get("url"),
        #         image=t["image"][-1]["#text"] if t.get("image") else None,
        #         # listeners=None
        #     )
        #     for t in raw_tracks
        # ]
        tracks=[]
        for t in raw_tracks:
            image = search_deezer_track_image(f"{t.get('name')} {t.get('artist', {}).get('name')}")
            tracks.append(Track(
                title=t["name"],
                artist=t["artist"]["name"],
                image=image,
            ))
        return tracks[:limit]
    except Exception as e:
        logger.warning(f"Error getting tracks for genre {tag_name}: {str(e)}")
        return []
    