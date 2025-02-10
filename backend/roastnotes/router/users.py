from fastapi import HTTPException, Depends
from sqlmodel import Session, select

from roastnotes.core.lib import FastApiRouter
from roastnotes.core.config import settings

from roastnotes.core.security import create_access_token, get_password_hash, verify_password
from roastnotes.core.db import get_session
from roastnotes.models.user import User
from roastnotes.schemas.response_models import DELETE_OK, RESPONSE_404
from roastnotes.schemas.security import Token
from roastnotes.schemas.user import UserCreate

router = FastApiRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/register", response_model=Token)
async def register_user(user: UserCreate, db: Session = Depends(get_session)) -> Token:
    if db.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        email=user.email, username=user.username, password_hash=get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=settings.JWT_EXPIRE_MINUTES
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login_user(user: UserCreate, db: Session = Depends(get_session)) -> Token:
    db_user: User | None = db.exec(select(User).where(User.email == user.email)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=settings.JWT_EXPIRE_MINUTES
    )

    return {"access_token": access_token, "token_type": "bearer"}


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