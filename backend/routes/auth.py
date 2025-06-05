from fastapi import APIRouter,HttpException

router= APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def register_user(username: str, password: str):
    """Register a new user and return access token"""

@router.post("/login")
async def login_user(username: str, password: str):
    """Login user and return access token"""

