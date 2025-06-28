from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging
from jose import JWTError, jwt
from schemas.user import UserCreate, UserLogin, Token, UserOut
from sqlalchemy.orm import Session
from db.session import get_db
from db.crud.user import user_crud
from utils.security import create_access_token, verify_password
from utils.config import settings


router = APIRouter(prefix="/auth", tags=["Authentication"])

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    scheme_name="User Authentication"
)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                              algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = user_crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user


@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Registration attempt for email: {user.email}")
        
        # Check for existing email
        db_user = user_crud.get_user_by_email(db, user.email)
        if db_user:
            logger.warning(f"Email already registered: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        # Check for existing username
        db_user = user_crud.get_user_by_username(db, user.username)
        if db_user:
            logger.warning(f"Username already registered: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Create new user
        new_user = user_crud.create_user(db=db, user=user)
        logger.info(f"Successfully registered user with ID: {new_user.id}")
        return new_user
        
    except HTTPException as he:
        # Re-raise HTTP exceptions as-is
        raise he
    except Exception as e:
        # Log unexpected errors and return 500
        logger.error(f"Registration failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        # Use email as username
        user = user_crud.get_user_by_email(db, email=form_data.username)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token using user's email
        access_token = create_access_token(data={"sub": user.email})
        logger.info(f"User {user.email} logged in successfully")
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise

@router.get("/me", response_model=UserOut)
async def read_current_user(current_user = Depends(get_current_user)):
    """Get current authenticated user's information"""
    return current_user
