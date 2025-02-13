from datetime import datetime
from typing import Optional

from sqlmodel import Session, select

from roastnotes.models.rating import Rating
from roastnotes.models.roast import Roast
from roastnotes.models.group_roast_collection import GroupRoastCollection
from roastnotes.models.groupmember import GroupMember
from roastnotes.schemas.rating import RatingCreate


class RatingManager:
    def __init__(self, session: Session):
        self.session = session

    def add_rating(self, user_id: int, rating_data: RatingCreate) -> Rating:
        # Start transaction
        with self.session.begin_nested():
            # Check for existing rating using SQLModel's select
            statement = select(Rating).where(
                Rating.user_id == user_id, Rating.roast_id == rating_data.roast_id
            )
            existing_rating = self.session.exec(statement).first()

            if existing_rating:
                # Update existing rating
                old_score = existing_rating.overall_score
                for field, value in rating_data.dict().items():
                    setattr(existing_rating, field, value)
                existing_rating.updated_at = datetime.utcnow()

                self._update_roast_stats(
                    rating_data.roast_id,
                    new_value=rating_data.overall_score,
                    old_value=old_score,
                    is_new=False,
                )
                
                self._update_group_stats(
                    user_id,
                    rating_data.roast_id,
                    rating_data.overall_score,
                    is_new=False,
                    old_value=old_score
                )
                return existing_rating

            # Create new rating
            new_rating = Rating(
                user_id=user_id,
                **rating_data.dict(),
                created_at=datetime.utcnow(),
            )
            self.session.add(new_rating)

            self._update_roast_stats(
                rating_data.roast_id,
                new_value=rating_data.overall_score,
                old_value=None,
                is_new=True,
            )

            self._update_group_stats(
                user_id,
                rating_data.roast_id,
                rating_data.overall_score,
                is_new=True,
            )

            return new_rating

    def _update_roast_stats(
        self, roast_id: int, new_value: float, old_value: Optional[float], is_new: bool
    ):
        statement = select(Roast).where(Roast.id == roast_id)
        roast = self.session.exec(statement).one()

        stats = roast.cached_rating_stats or {
            "total_ratings": 0,
            "avg_rating": 0,
            "last_updated": None,
        }

        current_total = stats["total_ratings"]
        current_avg = stats["avg_rating"]

        if is_new:
            new_total = current_total + 1
            new_avg = ((current_avg * current_total) + new_value) / new_total
        else:
            new_total = current_total
            new_avg = (
                (current_avg * current_total) - old_value + new_value
            ) / current_total

        roast.cached_rating_stats = {
            "total_ratings": new_total,
            "avg_rating": round(new_avg, 2),
            "last_updated": datetime.utcnow().isoformat(),
        }

    def _update_group_stats(
        self, user_id: int, roast_id: int, rating_value: float, is_new: bool, old_value: Optional[float] = None
    ):
        # Get all groups where this roast is collected and user is a member
        statement = (
            select(GroupRoastCollection)
            .join(GroupMember, GroupMember.group_id == GroupRoastCollection.group_id)
            .where(
                GroupRoastCollection.roast_id == roast_id,
                GroupMember.user_id == user_id,
            )
        )
        collections = self.session.exec(statement).all()

        for collection in collections:
            stats = collection.cached_group_rating_stats or {
                "total_ratings": 0,
                "avg_rating": 0,
                "last_updated": None,
            }

            if is_new:
                new_total = stats["total_ratings"] + 1
                new_avg = (
                    (stats["avg_rating"] * stats["total_ratings"]) + rating_value
                ) / new_total
            else:
                new_total = stats["total_ratings"]
                new_avg = (
                    (stats["avg_rating"] * stats["total_ratings"]) - old_value + rating_value
                ) / new_total

            collection.cached_group_rating_stats = {
                "total_ratings": new_total,
                "avg_rating": round(new_avg, 2),
                "last_updated": datetime.utcnow().isoformat(),
            }
