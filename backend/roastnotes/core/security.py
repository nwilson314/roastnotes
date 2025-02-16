from datetime import datetime, timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from loguru import logger
from passlib.context import CryptContext
from sqlmodel import Session, select

from roastnotes.core.config import settings
from roastnotes.core.db import get_session
from roastnotes.models.user import User
from roastnotes.schemas.response_models import AuthErrorResponse, AuthErrorSubCode

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: int | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)
) -> User:
    """
    Gets and validates the current user from the token provided.
    The token's 'sub' claim should contain the user's ID.
    """
    try:
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=AuthErrorResponse(
                    detail="Token has expired",
                    sub_code=AuthErrorSubCode.TOKEN_EXPIRED
                ).model_dump(),
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.PyJWTError as e:
            logger.warning(f"JWT validation failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=AuthErrorResponse(
                    detail="Could not validate credentials",
                    sub_code=AuthErrorSubCode.TOKEN_INVALID
                ).model_dump(),
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            logger.warning("Token payload missing 'sub' claim")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=AuthErrorResponse(
                    detail="Invalid token format",
                    sub_code=AuthErrorSubCode.TOKEN_INVALID
                ).model_dump(),
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        try:
            user_id = int(user_id_str)
        except ValueError:
            logger.warning(f"Token 'sub' claim is not a valid integer: {user_id_str}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=AuthErrorResponse(
                    detail="Invalid token format",
                    sub_code=AuthErrorSubCode.TOKEN_INVALID
                ).model_dump(),
                headers={"WWW-Authenticate": "Bearer"},
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in authentication: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthErrorResponse(
                detail="Authentication failed",
                sub_code=AuthErrorSubCode.TOKEN_INVALID
            ).model_dump(),
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.exec(select(User).where(User.id == user_id)).first()
    if user is None:
        logger.warning(f"No user found for ID {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthErrorResponse(
                detail="User not found",
                sub_code=AuthErrorSubCode.USER_NOT_FOUND
            ).model_dump(),
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return user
