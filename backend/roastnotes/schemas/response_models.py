from typing import Union, Any
from enum import Enum
from pydantic import BaseModel


class AuthErrorSubCode(str, Enum):
    """Specific authentication error codes for more granular error handling"""
    TOKEN_INVALID = "token_invalid"
    TOKEN_EXPIRED = "token_expired"
    USER_NOT_FOUND = "user_not_found"
    USER_UNAUTHORIZED = "user_unauthorized"


class ErrorResponse(BaseModel):
    """Base error response model"""
    status: int
    code: str
    detail: str
    sub_code: str | None = None


class AuthErrorResponse(ErrorResponse):
    """Authentication specific error response"""
    code: str = "authentication_failed"
    status: int = 401
    sub_code: AuthErrorSubCode


DELETE_OK: dict[str, bool] = {"ok": True}
RESPONSE_404: dict[Union[int, str], dict[str, Any]] = {
    404: {
        "description": "Item Not Found Error",
    },
}

# Common auth error responses
AUTH_ERROR_RESPONSES = {
    401: {
        "model": AuthErrorResponse,
        "description": "Authentication failed",
    }
}
