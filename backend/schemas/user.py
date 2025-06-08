from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserOut(UserBase):
    id: str
    
    class Config:
        orm_mode = True

class UserResponse(UserBase):
    id: str
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