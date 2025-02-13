from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel

from roastnotes.models.roast import RoastLevel
from roastnotes.schemas.roaster import RoasterResponse


class GroupRoastDetail(BaseModel):
    id: int
    name: str
    origin: str
    single_origin: bool
    roast_level: RoastLevel
    roaster: RoasterResponse
    added_by_username: str
    added_at: datetime
    notes: Optional[str]
    group_rating: Optional[float]  # from cached_group_rating_stats
    group_total_ratings: Optional[int]  # from cached_group_rating_stats
    global_rating: Optional[float]  # from roast.cached_rating_stats
    global_total_ratings: Optional[int]  # from roast.cached_rating_stats
    
    class Config:
        from_attributes = True


class GroupRoastCollection(BaseModel):
    group_name: str
    group_description: Optional[str]
    roasts: List[GroupRoastDetail]
    
    class Config:
        from_attributes = True


class UserGroupRoastsResponse(BaseModel):
    groups: Dict[str, GroupRoastCollection]  # key is group_id
