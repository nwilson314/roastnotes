from typing import Optional, List, TYPE_CHECKING, Dict
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from roastnotes.models.roast import Roast


class Roaster(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # Name of the roasting company/person
    location: str | None = None  # City, state, or address
    website: str | None = None  # Main website
    description: str | None = None  # Brief description or notes about the roaster
    social_media: Dict | None = Field(default=None, sa_column=Column(JSONB))  # Social media links and handles
    
    # Relationships
    roasts: List["Roast"] = Relationship(back_populates="roaster")
