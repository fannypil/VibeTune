from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    artist = Column(String)
    url = Column(String, nullable=True)
    playlist_id = Column(Integer, ForeignKey("playlists.id"))
    
    # Relationship
    playlist = relationship("Playlist", back_populates="tracks")