from typing import Optional, Dict

from pydantic import BaseModel


class RoasterBase(BaseModel):
    """Base schema with common roaster fields"""
    name: str
    location: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    social_media: Optional[Dict[str, str]] = None  # Platform -> URL/handle mapping


class RoasterCreate(RoasterBase):
    """Schema for creating a new roaster"""
    pass


class RoasterUpdate(BaseModel):
    """Schema for updating an existing roaster"""
    name: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    social_media: Optional[Dict[str, str]] = None


class RoasterResponse(RoasterBase):
    """Schema for roaster responses"""
    id: int
    
    class Config:
        from_attributes = True
