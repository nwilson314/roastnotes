from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

from roastnotes.models.group import Group
from roastnotes.models.rating import Rating

if TYPE_CHECKING:
    from roastnotes.models.user import User


class Roast(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    bean_details: str
    notes: Optional[str] = None
    ratings: list[Rating] = Relationship(back_populates="roast")
    user: Optional["User"] = Relationship(back_populates="roasts")
