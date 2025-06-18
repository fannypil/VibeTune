from sqlalchemy.orm import Session
from typing import Optional
from db.models.track import Track
from schemas.track import TrackCreate
import logging

logger = logging.getLogger(__name__)

class TrackCRUD:
    def add_track_to_playlist(self, db: Session, track: TrackCreate) -> Track:
        try:
            db_track = Track(
                name=track.name,
                artist=track.artist,
                url=track.url,
                playlist_id=track.playlist_id
            )
            db.add(db_track)
            db.commit()
            db.refresh(db_track)
            return db_track
        except Exception as e:
            db.rollback()
            logger.error(f"Error adding track: {str(e)}")
            raise

    def remove_track(self, db: Session, track_id: int) -> bool:
        try:
            track = db.query(Track).filter(Track.id == track_id).first()
            if track:
                db.delete(track)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"Error removing track: {str(e)}")
            raise

    def get_track(self, db: Session, track_id: int) -> Optional[Track]:
        return db.query(Track).filter(Track.id == track_id).first()

track_crud = TrackCRUD()