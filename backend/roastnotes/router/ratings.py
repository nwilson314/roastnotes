from fastapi import HTTPException, Depends
from sqlmodel import Session, select

from roastnotes.core.lib import FastApiRouter, update_model
from roastnotes.core.config import settings
from roastnotes.core.db import get_session
from roastnotes.models.rating import Rating
from roastnotes.schemas.rating import RatingCreate, RatingUpdate
from roastnotes.schemas.response_models import DELETE_OK, RESPONSE_404


router = FastApiRouter(
    prefix="/ratings",
    tags=["ratings"],
)


@router.get("/roast/{roast_id}")
def list_roast_ratings(
    roast_id: int,
    user_id: int | None = None,
    session: Session = Depends(get_session)
) -> list[Rating]:
    """Get all ratings for a roast, optionally filtered by user"""
    query = select(Rating).where(Rating.roast_id == roast_id)
    if user_id:
        query = query.where(Rating.user_id == user_id)
    return session.exec(query.order_by(Rating.created_at.desc())).all()


@router.post("/")
def create_rating(
    rating: RatingCreate, session: Session = Depends(get_session)
) -> Rating:
    # TODO: validate rating data?
    session.add(rating)
    session.commit()
    session.refresh(rating)
    return rating


@router.patch("/{rating_id}")
def update_rating(
    rating_id: int, rating: RatingUpdate, session: Session = Depends(get_session)
) -> Rating:
    db_rating = session.exec(select(Rating).where(Rating.id == rating_id)).first()
    if not db_rating:
        raise HTTPException(status_code=404, detail=RESPONSE_404)

    update_model(db_rating, rating, session)
    session.add(db_rating)
    session.commit()
    session.refresh(db_rating)
    return db_rating


@router.delete("/{rating_id}", response_model=dict[str, bool], responses=RESPONSE_404)
def delete_rating(rating_id: int, session: Session = Depends(get_session)) -> None:
    rating = session.exec(select(Rating).where(Rating.id == rating_id)).first()
    if not rating:
        raise HTTPException(status_code=404, detail=RESPONSE_404)

    session.delete(rating)
    session.commit()
    return DELETE_OK
