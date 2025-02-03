from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from roastnotes.models.roast import Roast
    from roastnotes.models.user import User


class GroupMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="group.id")
    user_id: int = Field(foreign_key="user.id")
    role: Optional[str] = None


class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    members: list["User"] = Relationship(
        back_populates="groups", link_model=GroupMember
    )
