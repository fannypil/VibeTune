from fastapi import APIRouter, HTTPException
from schemas import UserCreate, UserLogin, Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    """Dummy register endpoint"""
    return {
        "access_token": "dummy_token",
        "token_type": "bearer"
    }

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    """Dummy login endpoint"""
    return {
        "access_token": "dummy_token",
        "token_type": "bearer"
    }

# Dummy authentication for testing
async def get_current_user():
    return {"id": "dummy_user_id", "username": "dummy_user"}