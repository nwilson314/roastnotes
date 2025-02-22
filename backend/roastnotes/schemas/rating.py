from pydantic import BaseModel


class RatingCreate(BaseModel):
    roast_id: int
    user_id: int
    brew_method: str  # eg: v60, aeropress, moka pot, etc.
    preferred_method: bool = False  # user’s pick for this roast
    ratio: str  # water to coffee ratio
    temperature: float  # water temperature
    grind: str  # grind details
    tasting_notes: str | None = None  # coffee tasting notes
    overall_score: int  # out of 100


class RatingUpdate(BaseModel):
    brew_method: str | None = None  # user’s pick for this roast
    preferred_method: bool | None = None  # user’s pick for this roast
    ratio: str | None = None  # water to coffee ratio
    temperature: float | None = None  # water temperature
    grind: str | None = None  # grind details
    tasting_notes: str | None = None  # coffee tasting notes
    overall_score: int | None = None  # out of 100
