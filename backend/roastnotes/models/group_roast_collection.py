from datetime import datetime
from typing import Optional, TYPE_CHECKING, Dict, List

from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from roastnotes.models.group import Group
    from roastnotes.models.roast import Roast
    from roastnotes.models.user import User


class GroupRoastCollection(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="group.id")
    roast_id: int = Field(foreign_key="roast.id")
    added_by_user_id: int = Field(foreign_key="user.id")
    added_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None
    cached_group_rating_stats: Optional[Dict] = Field(
        default=None, sa_column=Column(JSON)
    )

    # Relationships
    group: "Group" = Relationship(back_populates="roast_collections")
    roast: "Roast" = Relationship(back_populates="group_collections")
    added_by: "User" = Relationship(back_populates="added_roast_collections")
