from datetime import datetime
from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship

from roastnotes.models.group import Group
from roastnotes.models.groupmember import GroupMember
from roastnotes.models.rating import Rating
from roastnotes.models.roast import Roast
from roastnotes.models.group_roast_collection import GroupRoastCollection


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, nullable=True, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str
    password_hash: Optional[str] = None  # placeholder for future auth
    created_at: datetime = Field(default_factory=datetime.utcnow)

    groups: List[Group] = Relationship(back_populates="users", link_model=GroupMember)
    roasts: List[Roast] = Relationship(back_populates="user")
    ratings: List[Rating] = Relationship(back_populates="user")
    added_roast_collections: List[GroupRoastCollection] = Relationship(
        back_populates="added_by"
    )
