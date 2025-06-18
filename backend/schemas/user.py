from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from .playlist import PlaylistOut

class UserBase(BaseModel):
    username: str = Field(..., min_length=3,
                           max_length=50,
                           description="Username must be between 3 and 50 characters")
    email: EmailStr = Field(..., description="Email must be a valid email address")
    first_name: str = Field(..., min_length=1
                            ,description="First name is required")
    last_name: str = Field(..., min_length=1,
                           description="Last name is required")
    
    @validator('email')
    def email_must_be_valid(cls, v):
        if not v:
            raise ValueError('Email address is required')
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8,
                           description="Password must be at least 8 characters long")
    @validator('password')
    def password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

class UserOut(UserBase):
    id: int
    playlists: List[PlaylistOut] = []
    favorites: List[PlaylistOut] = []
    
    class Config:
        orm_mode = True

class UserResponse(UserBase):
    id: int
    created_at: datetime
    favorite_genres: Optional[List[str]] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class TokenData(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    exp: Optional[datetime] = None