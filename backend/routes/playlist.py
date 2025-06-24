from fastapi import APIRouter, HTTPException, Depends, status
from schemas.playlist import PlaylistOut, PlaylistCreate, PlaylistUpdate, PlaylistSummary
from schemas.track import TrackCreate, TrackOut
from routes.auth import get_current_user
from db.crud.playlist import  playlist_crud
from db.session import get_db
from sqlalchemy.orm import Session
from typing import List
import logging


router = APIRouter(prefix="/playlist", tags=["Playlists"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=PlaylistOut)
async def create_playlist(
    playlist: PlaylistCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Add user_id to playlist data
        return playlist_crud.create_playlist(db, playlist, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/my-playlists", response_model=List[PlaylistSummary])
async def get_my_playlists(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    playlists = playlist_crud.get_user_playlists(db, current_user.id)
    return [
        PlaylistSummary(
            id=playlist.id,
            name=playlist.name,
            description=playlist.description,
            created_at=playlist.created_at,
            is_favorite=current_user in getattr(playlist, "favorited_by", [])
        )
        for playlist in playlists
    ]

@router.get("/favorites", response_model=List[PlaylistSummary])
async def get_favorite_playlists(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all playlists favorited by the current user"""
    playlists = playlist_crud.get_my_favorite_playlists(db, current_user.id)
    return [
    PlaylistSummary(
        id=playlist.id,
        name=playlist.name,
        description=playlist.description,
        created_at=playlist.created_at,
        is_favorite=True
    )
    for playlist in playlists
]

@router.get("/{playlist_id}", response_model=PlaylistOut)
async def get_playlist(
    playlist_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a playlist by ID"""
    try:
        logger.debug(f"Fetching playlist ID: {playlist_id}")
        playlist = playlist_crud.get_playlist(db, playlist_id)
        
        if not playlist:
            logger.warning(f"Playlist not found: {playlist_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Playlist not found"
            )
            
        logger.info(f"Successfully retrieved playlist: {playlist_id}")
         # Set is_favorite for this user
        playlist_out= PlaylistOut.from_orm(playlist)
        # Manually convert tracks
        playlist_out.tracks = [TrackOut.from_orm(track) for track in playlist.tracks]
        playlist_out.is_favorite = current_user in playlist.favorited_by
        return playlist_out
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving playlist: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.put("/{playlist_id}", response_model=PlaylistOut)
async def update_playlist(
    playlist_id: int,
    playlist: PlaylistUpdate, 
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        logger.debug(f"Updating playlist {playlist_id} with data: {playlist}")
        db_playlist = playlist_crud.get_playlist(db, playlist_id)
        
        if not db_playlist:
            logger.warning(f"Playlist not found: {playlist_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Playlist not found"
            )
            
        if db_playlist.user_id != current_user.id:
            logger.warning(f"Unauthorized update attempt for playlist {playlist_id} by user {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Not authorized to update this playlist"
            )
            
        updated_playlist = playlist_crud.update_playlist(db, playlist_id, playlist)
        logger.info(f"Successfully updated playlist {playlist_id}")
        return updated_playlist
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating playlist: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{playlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_playlist(
    playlist_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a playlist"""
    db_playlist = playlist_crud.get_playlist(db, playlist_id)
    if not db_playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    if db_playlist.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this playlist")
    playlist_crud.delete_playlist(db, playlist_id)



@router.post("/{playlist_id}/favorite", status_code=204)
async def favorite_playlist(
    playlist_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Favorite a playlist"""
    success = playlist_crud.favorite_playlist(db, playlist_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return

@router.delete("/{playlist_id}/favorite", status_code=204)
async def unfavorite_playlist(
    playlist_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Unfavorite a playlist"""
    success = playlist_crud.unfavorite_playlist(db, playlist_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return  

