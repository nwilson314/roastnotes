from pydantic import BaseModel
from roastnotes.schemas.user import UserResponse


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    token: Token
    user: UserResponse
