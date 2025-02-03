from fastapi import HTTPException, Depends
from sqlmodel import Session, select

from roastnotes.core.lib import FastApiRouter
from roastnotes.core.config import settings

# from roastnotes.core.security import create_access_token, get_password_hash, verify_password
from roastnotes.core.db import get_session
from roastnotes.models.user import User
from roastnotes.schemas.response_models import DELETE_OK, RESPONSE_404
# from roastnotes.schemas.security import Token
from roastnotes.schemas.user import UserCreate

router = FastApiRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/create", response_model=User)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    # Placeholder route for creating a user. Will be replaced with registration endpoint when user auth is implemented.
    if session.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=user.password # ... obviously not what we want
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user