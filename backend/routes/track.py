from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.crud.playlist import playlist_crud
from db.crud.track import track_crud
from db.session import get_db
from schemas.track import TrackCreate, TrackOut
from routes.auth import get_current_user
import logging


router = APIRouter(prefix="/track", tags=["Track"])
logger = logging.getLogger(__name__)


@router.post("/{playlist_id}/tracks", response_model=TrackOut)
async def add_track_to_playlist(
    playlist_id: int,
    track: TrackCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a track to a playlist"""
    try:
        # Check playlist exists and user owns it
        playlist = playlist_crud.get_playlist(db, playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")
        if playlist.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this playlist")

        # Add track
        track.playlist_id = playlist_id  # Ensure correct playlist ID
        return track_crud.add_track_to_playlist(db, track)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding track: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{playlist_id}/tracks/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_track_from_playlist(
    playlist_id: int,
    track_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a track from a playlist"""
    try:
        # Check playlist exists and user owns it
        playlist = playlist_crud.get_playlist(db, playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")
        if playlist.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this playlist")

        # Check track exists and belongs to playlist
        track = track_crud.get_track(db, track_id)
        if not track or track.playlist_id != playlist_id:
            raise HTTPException(status_code=404, detail="Track not found in playlist")

        track_crud.remove_track(db, track_id)
        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing track: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")