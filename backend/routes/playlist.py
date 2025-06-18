from fastapi import APIRouter, HTTPException, Depends, status
from schemas.playlist import PlaylistOut, PlaylistCreate, PlaylistUpdate
from routes.auth import get_current_user
from db.crud.playlist import PlaylistCRUD, playlist_crud
from db.session import get_db
from sqlalchemy.orm import Session
from typing import List
import logging


router = APIRouter(prefix="/playlist", tags=["Playlists"])
logger = logging.getLogger(__name__)



@router.post("/", response_model=PlaylistOut, status_code=status.HTTP_201_CREATED)
async def create_playlist(
    playlist: PlaylistCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new playlist"""
    return playlist_crud.create_playlist(db=db, playlist=playlist, user_id=current_user.id)


@router.get("/{playlist_id}", response_model=PlaylistOut)
async def get_playlist(
    playlist_id: int, 
    db: Session = Depends(get_db)
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
        return playlist
        
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
