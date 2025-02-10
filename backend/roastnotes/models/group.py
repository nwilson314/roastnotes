
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import Mapped

from roastnotes.models.groupmember import GroupMember

if TYPE_CHECKING:
    from roastnotes.models.user import User


class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    users: list["User"] = Relationship(back_populates="groups", link_model=GroupMember)