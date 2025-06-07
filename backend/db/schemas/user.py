from pydantic import BaseModel, EmailStr, Field
from .playlist import PlaylistOut
from typing import List, Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserOut(UserBase):
    id: int
    playlists: List[PlaylistOut] = []
    favorites: List[PlaylistOut] = []

    class Config:
        orm_mode = True
