from fastapi import HTTPException, Depends
from sqlmodel import Session, select
from loguru import logger

from roastnotes.core.lib import FastApiRouter
from roastnotes.core.config import settings

from roastnotes.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from roastnotes.core.db import get_session
from roastnotes.models.user import User
from roastnotes.schemas.response_models import DELETE_OK, RESPONSE_404
from roastnotes.schemas.security import AuthResponse, Token
from roastnotes.schemas.user import UserCreate, UserResponse, UserLogin

router = FastApiRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/register", response_model=AuthResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_session)) -> AuthResponse:
    if db.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        email=user.email,
        username=user.username,
        password_hash=get_password_hash(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(
        data={"sub": str(new_user.id)},
        expires_delta=settings.JWT_EXPIRE_MINUTES
    )

    return AuthResponse(
        token=Token(
            access_token=access_token,
            token_type="bearer",
        ),
        user=UserResponse.model_validate(new_user)
    )


@router.post("/login", response_model=AuthResponse)
async def login_user(user: UserLogin, db: Session = Depends(get_session)) -> AuthResponse:
    db_user: User | None = db.exec(select(User).where(User.email == user.email)).first()
    if not db_user:
        logger.warning(f"User {user.email} not found")
        raise HTTPException(status_code=404, detail="Invalid credentials")
    if not verify_password(user.password, db_user.password_hash):
        logger.warning(f"Invalid password for user {user.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=settings.JWT_EXPIRE_MINUTES
    )

    return AuthResponse(
        token=Token(
            access_token=access_token,
            token_type="bearer",
        ),
        user=UserResponse.model_validate(db_user)
    )


@router.delete("/delete", responses=RESPONSE_404)
async def delete_user(user: UserCreate, db: Session = Depends(get_session)) -> None:
    db_user = db.exec(select(User).where(User.email == user.email)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    # if not verify_password(user.password, db_user.hashed_password):
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    db.delete(db_user)
    db.commit()
    return DELETE_OK
