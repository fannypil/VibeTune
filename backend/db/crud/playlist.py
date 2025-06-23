from sqlalchemy.orm import Session
from typing import List, Optional
from db.models.playlist import Playlist
from schemas.playlist import PlaylistCreate, PlaylistUpdate
import logging

logger = logging.getLogger(__name__)

class PlaylistCRUD:
    def create_playlist(self, db: Session, playlist: PlaylistCreate, user_id: int) -> Playlist:
        try:
            logger.debug(f"Creating playlist '{playlist.name}' for user {user_id}")
            
            db_playlist = Playlist(
                name=playlist.name,
                description=playlist.description,
                # is_favorite=playlist.is_favorite,
                user_id=user_id
            )
            
            db.add(db_playlist)
            db.commit()
            db.refresh(db_playlist)
            
            logger.info(f"Successfully created playlist {db_playlist.id}")
            return db_playlist
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating playlist: {str(e)}", exc_info=True)
            raise
        
    def get_playlist(self, db: Session, playlist_id: int) -> Optional[Playlist]:
        try:
            logger.debug(f"Attempting to fetch playlist with ID: {playlist_id}")
            playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
            if playlist:
                logger.info(f"Found playlist: {playlist.id}")
            else:
                logger.warning(f"No playlist found with ID: {playlist_id}")
            return playlist
        except Exception as e:
            logger.error(f"Error fetching playlist {playlist_id}: {str(e)}", exc_info=True)
            raise


    def get_user_playlists(self, db: Session, user_id: int) -> List[Playlist]:
        return db.query(Playlist).filter(Playlist.user_id == user_id).all()

    def update_playlist(self, db: Session, playlist_id: int, playlist: PlaylistUpdate) -> Optional[Playlist]:
        db_playlist = self.get_playlist(db, playlist_id)
        if not db_playlist:
            return None
        
        for key, value in playlist.dict(exclude_unset=True).items():
            setattr(db_playlist, key, value)
        
        try:
            db.commit()
            db.refresh(db_playlist)
            return db_playlist
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating playlist: {str(e)}")
            raise

    def favorite_playlist(self, db: Session, playlist_id: int, user) -> bool:
        playlist = self.get_playlist(db, playlist_id)
        if not playlist:
            return False
        if user not in playlist.favorited_by:
            playlist.favorited_by.append(user)
            db.commit()
        return True
    
    def unfavorite_playlist(self, db: Session, playlist_id: int, user) -> bool:
        playlist = self.get_playlist(db, playlist_id)
        if not playlist:
            return False
        if user in playlist.favorited_by:
            playlist.favorited_by.remove(user)
            db.commit()
        return True
    
    def get_my_favorite_playlists(seld,db: Session, user_id: int):
        return db.query(Playlist).filter(Playlist.favorited_by.any(id=user_id)).all()

    def delete_playlist(self, db: Session, playlist_id: int) -> bool:
        db_playlist = self.get_playlist(db, playlist_id)
        if not db_playlist:
            return False
        
        try:
            db.delete(db_playlist)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting playlist: {str(e)}")
            raise
        

playlist_crud = PlaylistCRUD()

