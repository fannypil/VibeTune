from fastapi import APIRouter, HTTPException, Depends, status
from schemas.user import UserCreate, UserLogin, Token, UserOut
from sqlalchemy.orm import Session
from db.session import get_db
from db.crud.user import user_crud
from utils.security import create_access_token, verify_password
import logging



router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)


@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Registration attempt for email: {user.email}")
        
        # Check for existing user
        db_user = user_crud.get_user_by_email(db, user.email)
        if db_user:
            logger.warning(f"Email already registered: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        new_user = user_crud.create_user(db=db, user=user)
        logger.info(f"Successfully registered user with ID: {new_user.id}")
        return new_user
        
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, credentials.email)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# Dummy authentication for testing
async def get_current_user():
    return {"id": "dummy_user_id", "username": "dummy_user"}