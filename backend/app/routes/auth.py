from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import AdminUser, User
from app.schemas.schemas import Token, UserLogin, UserRegister, UserResponse, CitizenRegister, CitizenResponse
from app.utils.auth import verify_password, create_access_token, get_password_hash, settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    """
    Registers a new authorized officer/administrator.
    """
    # Check if username or email already exists
    existing_user = db.query(AdminUser).filter(
        (AdminUser.username == payload.username) | (AdminUser.email == payload.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is already registered."
        )

    hashed_password = get_password_hash(payload.password)
    db_user = AdminUser(
        username=payload.username,
        full_name=payload.full_name,
        email=payload.email,
        department=payload.department,
        role=payload.role,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2 compatible token login, returning a JWT access token.
    """
    user = db.query(AdminUser).filter(AdminUser.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "username": user.username
    }

@router.post("/citizen/register", response_model=CitizenResponse, status_code=status.HTTP_201_CREATED)
def citizen_register(payload: CitizenRegister, db: Session = Depends(get_db)):
    """
    Registers a new citizen user account.
    """
    existing_user = db.query(User).filter(
        (User.username == payload.username) | (User.email == payload.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is already registered."
        )

    hashed_password = get_password_hash(payload.password)
    db_citizen = User(
        username=payload.username,
        email=payload.email,
        password_hash=hashed_password
    )
    db.add(db_citizen)
    db.commit()
    db.refresh(db_citizen)
    return db_citizen

@router.post("/citizen/login", response_model=Token)
def citizen_login(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Standard user/citizen login, returning a JWT token.
    """
    citizen = db.query(User).filter(User.username == payload.username).first()
    if not citizen or not verify_password(payload.password, citizen.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": citizen.username, "role": "Citizen"},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": "Citizen",
        "username": citizen.username
    }
