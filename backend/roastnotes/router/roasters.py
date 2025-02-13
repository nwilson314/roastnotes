from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from loguru import logger

from roastnotes.core.db import get_session
from roastnotes.core.security import get_current_user
from roastnotes.models.roaster import Roaster
from roastnotes.models.user import User
from roastnotes.schemas.roaster import RoasterCreate, RoasterUpdate, RoasterResponse

router = APIRouter(prefix="/roasters", tags=["roasters"])


@router.get("/", response_model=list[RoasterResponse])
def list_roasters(
    search: str | None = Query(None, description="Search roaster names"),
    session: Session = Depends(get_session),
) -> list[RoasterResponse]:
    """
    List all roasters, optionally filtered by a search term.
    """
    try:
        query = select(Roaster)
        if search:
            query = query.where(Roaster.name.ilike(f"%{search}%"))
        roasters = session.exec(query).all()
        logger.info(f"Retrieved {len(roasters)} roasters")
        return roasters
    except Exception as e:
        logger.error(f"Failed to list roasters: {str(e)}")
        raise


@router.post("/", response_model=RoasterResponse)
def create_roaster(
    roaster: RoasterCreate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),  # Require authentication
) -> RoasterResponse:
    """
    Create a new roaster.
    """
    try:
        # Check if roaster with same name exists
        existing = session.exec(
            select(Roaster).where(Roaster.name == roaster.name)
        ).first()
        if existing:
            logger.warning(f"Roaster with name {roaster.name} already exists")
            raise HTTPException(
                status_code=400,
                detail=f"Roaster with name {roaster.name} already exists"
            )
            
        db_roaster = Roaster.model_validate(roaster)
        session.add(db_roaster)
        session.commit()
        session.refresh(db_roaster)
        logger.info(f"Created roaster {db_roaster.name} (id: {db_roaster.id})")
        return db_roaster
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create roaster: {str(e)}")
        raise


@router.get("/{roaster_id}", response_model=RoasterResponse)
def get_roaster(
    roaster_id: int,
    session: Session = Depends(get_session),
) -> RoasterResponse:
    """
    Get a specific roaster by ID.
    """
    try:
        roaster = session.exec(
            select(Roaster).where(Roaster.id == roaster_id)
        ).first()
        if not roaster:
            logger.warning(f"Roaster {roaster_id} not found")
            raise HTTPException(
                status_code=404,
                detail=f"Roaster {roaster_id} not found"
            )
        return roaster
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get roaster {roaster_id}: {str(e)}")
        raise


@router.patch("/{roaster_id}", response_model=RoasterResponse)
def update_roaster(
    roaster_id: int,
    roaster_update: RoasterUpdate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),  # Require authentication
) -> RoasterResponse:
    """
    Update a roaster's information.
    """
    try:
        db_roaster = session.exec(
            select(Roaster).where(Roaster.id == roaster_id)
        ).first()
        if not db_roaster:
            logger.warning(f"Roaster {roaster_id} not found")
            raise HTTPException(
                status_code=404,
                detail=f"Roaster {roaster_id} not found"
            )
            
        # Check if name change would conflict
        if (
            roaster_update.name is not None 
            and roaster_update.name != db_roaster.name
        ):
            existing = session.exec(
                select(Roaster).where(Roaster.name == roaster_update.name)
            ).first()
            if existing:
                logger.warning(
                    f"Cannot update roaster {roaster_id}: "
                    f"name {roaster_update.name} already exists"
                )
                raise HTTPException(
                    status_code=400,
                    detail=f"Roaster with name {roaster_update.name} already exists"
                )
        
        roaster_data = roaster_update.model_dump(exclude_unset=True)
        for key, value in roaster_data.items():
            setattr(db_roaster, key, value)
            
        session.add(db_roaster)
        session.commit()
        session.refresh(db_roaster)
        logger.info(f"Updated roaster {roaster_id}")
        return db_roaster
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update roaster {roaster_id}: {str(e)}")
        raise
