from datetime import datetime
from typing import Optional, TYPE_CHECKING, List

from sqlmodel import Field, SQLModel, Relationship

from roastnotes.models.groupmember import GroupMember

if TYPE_CHECKING:
    from roastnotes.models.user import User
    from roastnotes.models.group_roast_collection import GroupRoastCollection


class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    users: List["User"] = Relationship(back_populates="groups", link_model=GroupMember)
    roast_collections: List["GroupRoastCollection"] = Relationship(
        back_populates="group"
    )
