from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from schemas.user import UserOut
from db.crud.user import user_crud
import logging

router = APIRouter(prefix="/users", tags=["Users"])
logger = logging.getLogger(__name__)

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID (admin only)"""
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users (admin only)"""
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user (admin only)"""
    success = user_crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None  # Explicitly return None for 204