from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from roastnotes.models.roast import Roast
    from roastnotes.models.user import User


class Rating(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    roast_id: int = Field(foreign_key="roast.id")
    user_id: int = Field(foreign_key="user.id")
    brew_method: str  # eg: v60, aeropress, moka pot, etc.
    preferred_method: bool = False  # user’s pick for this roast
    ratio: str  # water to coffee ratio
    temperature: float  # water temperature
    grind: str  # grind details
    tasting_notes: Optional[str] = None  # coffee tasting notes
    overall_score: int  # out of 100
    created_at: datetime = Field(default_factory=datetime.utcnow)
    roast: Optional["Roast"] = Relationship(back_populates="ratings")
    user: Optional["User"] = Relationship(back_populates="ratings")
