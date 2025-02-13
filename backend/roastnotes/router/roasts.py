from datetime import datetime

from fastapi import HTTPException, Depends
from sqlmodel import Session, select
from loguru import logger

from roastnotes.core.lib import FastApiRouter, update_model
from roastnotes.core.config import settings
from roastnotes.core.db import get_session
from roastnotes.core.security import get_current_user
from roastnotes.models.group_roast_collection import GroupRoastCollection
from roastnotes.models.rating import Rating
from roastnotes.models.roast import Roast, BeanDetails
from roastnotes.models.user import User
from roastnotes.services.rating_manager import RatingManager
from roastnotes.schemas.response_models import DELETE_OK, RESPONSE_404
from roastnotes.schemas.rating import RatingCreate
from roastnotes.schemas.roast import RoastCreate, RoastUpdate
from roastnotes.schemas.group_roast import GroupRoastDetail

router = FastApiRouter(
    prefix="/roasts",
    tags=["roasts"],
)


@router.get("/")
def list_roasts(session: Session = Depends(get_session)) -> list[Roast]:
    """
    Get all roasts
    For now this is used as a unauthenticated endpoint to get trending roasts
    """
    # TODO: add pagination
    # TODO: add sorting
    # TODO: get better trending highlights
    return session.exec(select(Roast)).all()


@router.get("/{roast_id}")
def get_roast(roast_id: int, session: Session = Depends(get_session)) -> Roast:
    roast = session.exec(select(Roast).where(Roast.id == roast_id)).first()
    if not roast:
        logger.warning(f"Roast {roast_id} not found")
        raise HTTPException(status_code=404, detail=RESPONSE_404)
    return roast


@router.post("/")
def create_roast(
    roast_data: RoastCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Roast:
    """Create a new roast"""
    try:
        # Create the roast
        roast = Roast(
            user_id=current_user.id,
            roaster_id=roast_data.roaster_id,
            name=roast_data.name,
            origin=roast_data.origin,
            single_origin=roast_data.single_origin,
            roast_level=roast_data.roast_level,
        )
        session.add(roast)
        session.commit()
        session.refresh(roast)
        
        # Add bean details if provided
        if roast_data.bean_details:
            bean_details = BeanDetails(
                roast_id=roast.id,
                **roast_data.bean_details.model_dump()
            )
            session.add(bean_details)
            session.commit()
            session.refresh(roast)  # Refresh to get the bean_details relationship
            
        logger.info(f"Created new roast: {roast.name} (id: {roast.id})")
        return roast
    except Exception as e:
        logger.error(f"Failed to create roast: {str(e)}")
        raise


@router.post("/groups/{group_id}/roasts")
def add_roast_to_group(
    group_id: int,
    roast_id: int,
    notes: str | None = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> GroupRoastCollection:
    try:
        # Verify roast exists
        roast = session.exec(select(Roast).where(Roast.id == roast_id)).first()
        if not roast:
            logger.warning(f"Cannot add roast {roast_id} to group {group_id}: roast not found")
            raise HTTPException(status_code=404, detail=f"Roast {roast_id} not found")
            
        collection = GroupRoastCollection(
            group_id=group_id,
            roast_id=roast_id,
            added_by_user_id=current_user.id,
            notes=notes,
            cached_group_rating_stats={
                "total_ratings": 0,
                "avg_rating": 0,
                "last_updated": datetime.utcnow().isoformat(),
            },
        )
        session.add(collection)
        session.commit()
        session.refresh(collection)
        logger.info(f"Added roast {roast_id} to group {group_id} by user {current_user.id}")
        return collection
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to add roast {roast_id} to group {group_id}: {str(e)}")
        raise


@router.post("/rate")
def rate_roast(
    rating: RatingCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Rating:
    try:
        rating_manager = RatingManager(session)
        rating = rating_manager.add_rating(rating)
        session.commit()
        logger.info(f"User {current_user.id} rated roast {rating.roast_id} with score {rating.overall_score}")
        return rating
    except Exception as e:
        logger.error(f"Failed to add rating for roast {rating.roast_id}: {str(e)}")
        raise


@router.get("/groups/{group_id}/roasts")
def list_group_roasts(
    group_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> list[GroupRoastDetail]:
    """Get all roasts for a specific group with both group and global stats"""
    collections = session.exec(
        select(GroupRoastCollection)
        .where(GroupRoastCollection.group_id == group_id)
        .order_by(GroupRoastCollection.added_at.desc())
    ).all()
    
    return [
        GroupRoastDetail(
            id=collection.roast_id,
            name=collection.roast.name,
            origin=collection.roast.origin,
            single_origin=collection.roast.single_origin,
            roast_level=collection.roast.roast_level,
            roaster=collection.roast.roaster,
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


@router.get("/groups/{group_id}/roasts/{roast_id}")
def get_group_roast(
    group_id: int,
    roast_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> GroupRoastDetail:
    """Get a specific roast in a group context with both group and global stats"""
    collection = session.exec(
        select(GroupRoastCollection)
        .where(GroupRoastCollection.group_id == group_id)
        .where(GroupRoastCollection.roast_id == roast_id)
    ).first()
    
    if not collection:
        logger.warning(f"Roast {roast_id} not found in group {group_id}")
        raise HTTPException(status_code=404, detail=RESPONSE_404)
    
    return GroupRoastDetail(
        id=collection.roast_id,
        name=collection.roast.name,
        origin=collection.roast.origin,
        single_origin=collection.roast.single_origin,
        roast_level=collection.roast.roast_level,
        roaster=collection.roast.roaster,
        added_by_username=collection.added_by.username,
        added_at=collection.added_at,
        notes=collection.notes,
        group_rating=collection.cached_group_rating_stats["avg_rating"] if collection.cached_group_rating_stats else None,
        group_total_ratings=collection.cached_group_rating_stats["total_ratings"] if collection.cached_group_rating_stats else None,
        global_rating=collection.roast.cached_rating_stats["avg_rating"] if collection.roast.cached_rating_stats else None,
        global_total_ratings=collection.roast.cached_rating_stats["total_ratings"] if collection.roast.cached_rating_stats else None,
    )


@router.patch("/{roast_id}")
def update_roast(
    roast_id: int, roast: RoastUpdate, session: Session = Depends(get_session)
) -> Roast:
    db_roast = session.exec(select(Roast).where(Roast.id == roast_id)).first()
    if not db_roast:
        logger.warning(f"Cannot update roast {roast_id}: not found")
        raise HTTPException(status_code=404, detail=RESPONSE_404)
    
    try:
        update_model(db_roast, roast)
        session.add(db_roast)
        session.commit()
        session.refresh(db_roast)
        logger.info(f"Updated roast {roast_id}")
        return db_roast
    except Exception as e:
        logger.error(f"Failed to update roast {roast_id}: {str(e)}")
        raise


@router.delete("/{roast_id}", response_model=dict[str, bool], responses=RESPONSE_404)
def delete_roast(roast_id: int, session: Session = Depends(get_session)) -> None:
    roast = session.exec(select(Roast).where(Roast.id == roast_id)).first()
    if not roast:
        logger.warning(f"Cannot delete roast {roast_id}: not found")
        raise HTTPException(status_code=404, detail=RESPONSE_404)
    
    try:
        session.delete(roast)
        session.commit()
        logger.info(f"Deleted roast {roast_id}")
        return {"ok": True}
    except Exception as e:
        logger.error(f"Failed to delete roast {roast_id}: {str(e)}")
        raise
