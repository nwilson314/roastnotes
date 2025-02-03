from pydantic import BaseModel


class RoastCreate(BaseModel):
    sender_id: int
    bean_details: str
    notes: str | None = None


class RoastUpdate(BaseModel):
    bean_details: str | None = None
    notes: str | None = None