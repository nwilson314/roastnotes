from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel

from roastnotes.models.roast import RoastLevel


class BeanDetailsCreate(BaseModel):
    """Schema for creating bean details"""
    species: str
    cultivar: Optional[str] = None
    processing_method: Optional[str] = None
    altitude: Optional[int] = None
    extra: Optional[dict] = None


class BeanDetailsUpdate(BaseModel):
    """Schema for updating bean details"""
    species: Optional[str] = None
    cultivar: Optional[str] = None
    processing_method: Optional[str] = None
    altitude: Optional[int] = None
    extra: Optional[dict] = None


class BeanDetailsResponse(BaseModel):
    """Schema for bean details in responses"""
    species: str
    cultivar: Optional[str] = None
    processing_method: Optional[str] = None
    altitude: Optional[int] = None
    extra: Optional[dict] = None

    class Config:
        from_attributes = True


class RoastCreate(BaseModel):
    """Schema for creating a new roast"""
    roaster_id: int  # Required: must specify which roaster made this coffee
    name: str  # Required: name of the roast/blend
    origin: str  # Required: country or region of origin
    single_origin: bool = False
    roast_level: RoastLevel = RoastLevel.unspecified
    bean_details: Optional[BeanDetailsCreate] = None  # Optional: can add bean details later


class RoastUpdate(BaseModel):
    """Schema for updating an existing roast"""
    name: Optional[str] = None
    origin: Optional[str] = None
    single_origin: Optional[bool] = None
    roast_level: Optional[RoastLevel] = None
    bean_details: Optional[BeanDetailsUpdate] = None


class RoastResponse(BaseModel):
    """Schema for roast responses"""
    id: int
    name: str
    origin: str
    single_origin: bool
    roast_level: RoastLevel
    created_at: datetime
    cached_rating_stats: Optional[Dict] = None
    bean_details: Optional[BeanDetailsResponse] = None

    class Config:
        from_attributes = True
