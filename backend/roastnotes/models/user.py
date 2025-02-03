from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship

from roastnotes.models.group import Group, GroupMember
from roastnotes.models.rating import Rating
from roastnotes.models.roast import Roast


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str
    password_hash: Optional[str] = None  # placeholder for future auth
    created_at: datetime = Field(default_factory=datetime.utcnow)
    groups: list[Group] = Relationship(back_populates="members", link_model=GroupMember)
    roasts: list[Roast] = Relationship(back_populates="sender")
    ratings: list[Rating] = Relationship(back_populates="user")
