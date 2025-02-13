from fastapi import HTTPException, Depends, Query
from sqlmodel import Session, select, func
from typing import Optional, Dict
from loguru import logger

from roastnotes.core.lib import FastApiRouter
from roastnotes.core.config import settings
from roastnotes.core.db import get_session
from roastnotes.core.security import get_current_user
from roastnotes.models.group import Group
from roastnotes.models.groupmember import GroupMember
from roastnotes.models.group_roast_collection import GroupRoastCollection
from roastnotes.models.user import User
from roastnotes.schemas.response_models import DELETE_OK, RESPONSE_404
from roastnotes.schemas.group import UserGroupResponse
from roastnotes.schemas.group_roast import GroupRoastDetail, GroupRoastCollection as GroupRoastCollectionResponse, UserGroupRoastsResponse

router = FastApiRouter(
    prefix="/groups",
    tags=["groups"],
)


@router.get("/")
def list_groups(session: Session = Depends(get_session)) -> list[Group]:
    try:
        return session.exec(select(Group)).all()
    except Exception as e:
        logger.error(f"Failed to list groups: {str(e)}")
        raise


@router.post("/")
def create_group(group: Group, session: Session = Depends(get_session)) -> Group:
    try:
        session.add(group)
        session.commit()
        session.refresh(group)
        logger.info(f"Created new group: {group.name} (id: {group.id})")
        return group
    except Exception as e:
        logger.error(f"Failed to create group: {str(e)}")
        raise


@router.get("/{group_id}/members")
def list_group_members(
    group_id: int, session: Session = Depends(get_session)
) -> list[GroupMember]:
    try:
        return session.exec(
            select(GroupMember).where(GroupMember.group_id == group_id)
        ).all()
    except Exception as e:
        logger.error(f"Failed to list members for group {group_id}: {str(e)}")
        raise


@router.post("/{group_id}/members")
def add_group_member(
    group_id: int, group_member: GroupMember, session: Session = Depends(get_session)
) -> GroupMember:
    try:
        # Verify group exists
        group = session.exec(select(Group).where(Group.id == group_id)).first()
        if not group:
            logger.warning(f"Cannot add member to group {group_id}: group not found")
            raise HTTPException(status_code=404, detail=f"Group {group_id} not found")
            
        # Verify user exists
        user = session.exec(select(User).where(User.id == group_member.user_id)).first()
        if not user:
            logger.warning(f"Cannot add user {group_member.user_id} to group {group_id}: user not found")
            raise HTTPException(status_code=404, detail=f"User {group_member.user_id} not found")
            
        # Check if already a member
        existing = session.exec(
            select(GroupMember)
            .where(GroupMember.group_id == group_id)
            .where(GroupMember.user_id == group_member.user_id)
        ).first()
        if existing:
            logger.warning(f"User {group_member.user_id} is already a member of group {group_id}")
            raise HTTPException(status_code=400, detail="User is already a member of this group")
            
        group_member.group_id = group_id
        session.add(group_member)
        session.commit()
        session.refresh(group_member)
        logger.info(f"Added user {group_member.user_id} to group {group_id}")
        return group_member
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to add member to group {group_id}: {str(e)}")
        raise


@router.get("/user/{user_id}", response_model=list[UserGroupResponse])
def list_user_groups(
    user_id: int,
    include_stats: bool = Query(False, description="Include member and roast counts"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[UserGroupResponse]:
    """
    Get all groups that a specific user is a member of.
    Optionally includes member count and roast count for each group.
    """
    # Verify user exists
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        logger.warning(f"Cannot list groups for user {user_id}: user not found")
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    try:
        # Base query to get groups and stats
        query = (
            select(
                Group,
                func.count(func.distinct(GroupMember.user_id)).label("member_count") if include_stats else None,
                func.count(func.distinct(GroupRoastCollection.roast_id)).label("roast_count") if include_stats else None,
            )
            .join(GroupMember)
            .where(GroupMember.user_id == user_id)
        )
        
        # Add stats if requested
        if include_stats:
            query = (
                query
                .join(GroupMember, Group.id == GroupMember.group_id, isouter=True)
                .join(GroupRoastCollection, Group.id == GroupRoastCollection.group_id, isouter=True)
                .group_by(Group.id)
            )
        
        results = session.exec(query).all()
        logger.info(f"Retrieved {len(results)} groups for user {user_id}")
        
        return [
            UserGroupResponse(
                id=group.id,
                name=group.name,
                description=group.description,
                member_count=member_count if include_stats else None,
                roast_count=roast_count if include_stats else None,
            )
            for group, member_count, roast_count in results
        ]
    except Exception as e:
        logger.error(f"Failed to list groups for user {user_id}: {str(e)}")
        raise


@router.get("/user/{user_id}/roasts", response_model=UserGroupRoastsResponse)
def list_user_group_roasts(
    user_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> UserGroupRoastsResponse:
    """
    Get all roasts from groups that a specific user is a member of,
    organized by group with both group-specific and global stats.
    """
    # Verify user exists
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        logger.warning(f"Cannot list group roasts for user {user_id}: user not found")
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    try:
        # Get all groups the user is a member of
        groups = session.exec(
            select(Group)
            .join(GroupMember)
            .where(GroupMember.user_id == user_id)
        ).all()
        
        # Build response with roasts for each group
        group_roasts: Dict[str, GroupRoastCollectionResponse] = {}
        
        for group in groups:
            collections = session.exec(
                select(GroupRoastCollection)
                .where(GroupRoastCollection.group_id == group.id)
                .order_by(GroupRoastCollection.added_at.desc())
            ).all()
            
            if collections:  # Only include groups that have roasts
                roasts = [
                    GroupRoastDetail(
                        id=collection.roast_id,
                        name=collection.roast.name,
                        origin=collection.roast.origin,
                        added_by_username=collection.added_by.username,
                        added_at=collection.added_at,
                        notes=collection.notes,
                        group_rating=collection.cached_group_rating_stats["avg_rating"] if collection.cached_group_rating_stats else None,
                        group_total_ratings=collection.cached_group_rating_stats["total_ratings"] if collection.cached_group_rating_stats else None,
                        global_rating=collection.roast.cached_rating_stats["avg_rating"] if collection.roast.cached_rating_stats else None,
                        global_total_ratings=collection.roast.cached_rating_stats["total_ratings"] if collection.roast.cached_rating_stats else None,
                    )
                    for collection in collections
                ]
                
                group_roasts[str(group.id)] = GroupRoastCollectionResponse(
                    group_name=group.name,
                    group_description=group.description,
                    roasts=roasts
                )
        
        logger.info(f"Retrieved roasts from {len(group_roasts)} groups for user {user_id}")
        return UserGroupRoastsResponse(groups=group_roasts)
    except Exception as e:
        logger.error(f"Failed to list group roasts for user {user_id}: {str(e)}")
        raise


@router.delete("/{group_id}", response_model=dict[str, bool], responses=RESPONSE_404)
def delete_group(group_id: int, session: Session = Depends(get_session)) -> None:
    group = session.exec(select(Group).where(Group.id == group_id)).first()
    if not group:
        logger.warning(f"Cannot delete group {group_id}: not found")
        raise HTTPException(status_code=404, detail=RESPONSE_404)
    
    try:
        session.delete(group)
        session.commit()
        logger.info(f"Deleted group {group_id}")
        return {"ok": True}
    except Exception as e:
        logger.error(f"Failed to delete group {group_id}: {str(e)}")
        raise
