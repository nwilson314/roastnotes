from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserGroupResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    member_count: Optional[int]
    roast_count: Optional[int]
    
    class Config:
        from_attributes = True  # for SQLAlchemy compatibility
