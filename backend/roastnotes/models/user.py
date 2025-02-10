
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

from roastnotes.models.group import Group
from roastnotes.models.groupmember import GroupMember
from roastnotes.models.rating import Rating
from roastnotes.models.roast import Roast


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, nullable=True, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str
    password_hash: Optional[str] = None  # placeholder for future auth
    created_at: datetime = Field(default_factory=datetime.utcnow)
    groups: list[Group] = Relationship(
        back_populates="users",
        link_model=GroupMember
    )
    roasts: list[Roast] = Relationship(
        back_populates="user"
    )
    ratings: list[Rating] = Relationship(
        back_populates="user"
    )
