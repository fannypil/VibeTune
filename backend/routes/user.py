from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from db.schemas.user import UserCreate, UserOut
from db.crud.user import user_crud
import logging
import traceback


router = APIRouter(prefix="/users", tags=["Users"])

logger = logging.getLogger(__name__)

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Attempting to create user with email: {user.email}")
        
        # Check if email exists
        if user_crud.get_user_by_email(db, user.email):
            logger.warning(f"Email already registered: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        new_user = user_crud.create_user(db=db, user=user)
        logger.info(f"Successfully created user with ID: {new_user.id}")
        return new_user
        
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not create user: {str(e)}"
        )

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users with pagination"""
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users