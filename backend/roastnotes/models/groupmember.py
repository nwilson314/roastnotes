from sqlmodel import SQLModel, Field


class GroupMember(SQLModel, table=True):
    group_id: int | None = Field(default=None, foreign_key="group.id", primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)