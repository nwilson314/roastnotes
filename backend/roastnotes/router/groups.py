from fastapi import HTTPException, Depends
from sqlmodel import Session, select

from roastnotes.core.lib import FastApiRouter
from roastnotes.core.config import settings
from roastnotes.core.db import get_session
from roastnotes.models.group import Group, GroupMember
from roastnotes.schemas.response_models import DELETE_OK, RESPONSE_404


router = FastApiRouter(
    prefix="/groups",
    tags=["groups"],
)


@router.get("/")
def list_groups(session: Session = Depends(get_session)) -> list[Group]:
    return session.exec(select(Group)).all()


@router.post("/")
def create_group(group: Group, session: Session = Depends(get_session)) -> Group:
    # TODO: validate group data?
    session.add(group)
    session.commit()
    session.refresh(group)
    return group


@router.get("/{group_id}/members")
def list_group_members(group_id: int, session: Session = Depends(get_session)) -> list[GroupMember]:
    return session.exec(select(GroupMember).where(GroupMember.group_id == group_id)).all()

@router.post("/{group_id}/members")
def add_group_member(group_id: int, group_member: GroupMember, session: Session = Depends(get_session)) -> GroupMember:
    # TODO: validate group member data?
    # does the group member need to be created before it is added? Or is that handled by sqlmodel?
    group_member.group_id = group_id
    session.add(group_member)
    session.commit()
    session.refresh(group_member)
    return group_member


@router.delete("/{group_id}", response_model=dict[str, bool], responses=RESPONSE_404)
def delete_group(group_id: int, session: Session = Depends(get_session)) -> None:
    group = session.exec(select(Group).where(Group.id == group_id)).first()
    if not group:
        raise HTTPException(status_code=404, detail=RESPONSE_404)
    
    session.delete(group)
    session.commit()
    return DELETE_OK