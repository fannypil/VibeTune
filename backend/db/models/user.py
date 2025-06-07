from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

# Association table for user favorites
user_favorites = Table(
    'user_favorites',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('playlist_id', Integer, ForeignKey('playlists.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationships
    playlists = relationship("Playlist", back_populates="owner")
    favorites = relationship(
        "Playlist",
        secondary=user_favorites,
        back_populates="favorited_by"
    )
