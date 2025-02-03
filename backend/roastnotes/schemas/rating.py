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