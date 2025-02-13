from datetime import datetime
import enum
from typing import Optional, TYPE_CHECKING, Dict, List

from sqlalchemy import Enum, Column, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel, Relationship

from roastnotes.models.roaster import Roaster
from roastnotes.models.rating import Rating

if TYPE_CHECKING:
    from roastnotes.models.user import User
    from roastnotes.models.group_roast_collection import GroupRoastCollection


class RoastLevel(str, enum.Enum):
    unspecified = "unspecified"
    light = "light"
    medium = "medium"
    dark = "dark"


class BeanDetails(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    roast_id: int = Field(foreign_key="roast.id")
    species: str
    cultivar: str | None = None
    processing_method: str | None = None
    altitude: int | None = None
    extra: dict | None = Field(default=None, sa_column=Column(JSONB))
    roast: Optional["Roast"] = Relationship(back_populates="bean_details")


class Roast(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  # User who created this entry
    roaster_id: int = Field(foreign_key="roaster.id")  # Roaster who made this coffee
    name: str  # Name of the roast/blend
    origin: str  # Country or region of origin
    single_origin: bool = False
    roast_level: RoastLevel = Field(
        default=RoastLevel.unspecified, sa_column=Column(Enum(RoastLevel))
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    cached_rating_stats: Optional[Dict] = Field(default=None, sa_column=Column(JSON))

    # Relationships
    bean_details: Optional[BeanDetails] = Relationship(back_populates="roast")
    ratings: List[Rating] = Relationship(back_populates="roast")
    user: Optional["User"] = Relationship(back_populates="roasts")
    roaster: Optional[Roaster] = Relationship(back_populates="roasts")
    group_collections: List["GroupRoastCollection"] = Relationship(
        back_populates="roast"
    )
