from fastapi import HTTPException, Depends
from sqlmodel import Session, select

from roastnotes.core.lib import FastApiRouter, update_model
from roastnotes.core.config import settings
from roastnotes.core.db import get_session
from roastnotes.models.roast import Roast
from roastnotes.schemas.response_models import DELETE_OK, RESPONSE_404
from roastnotes.schemas.roast import RoastCreate, RoastUpdate


router = FastApiRouter(
    prefix="/roasts",
    tags=["roasts"],
)


@router.get("/")
def list_roasts(session: Session = Depends(get_session)) -> list[Roast]:
    # TODO: add pagination
    # TODO: add sorting
    return session.exec(select(Roast)).all()

@router.post("/")
def create_roast(roast: RoastCreate, session: Session = Depends(get_session)) -> Roast:
    # TODO: validate roast data?
    session.add(roast)
    session.commit()
    session.refresh(roast)
    return roast

@router.get("/{roast_id}")
def get_roast(roast_id: int, session: Session = Depends(get_session)) -> Roast:
    roast = session.exec(select(Roast).where(Roast.id == roast_id)).first()
    if not roast:
        raise HTTPException(status_code=404, detail=RESPONSE_404)
    return roast

@router.patch("/{roast_id}")
def update_roast(roast_id: int, roast: RoastUpdate, session: Session = Depends(get_session)) -> Roast:
    db_roast = session.exec(select(Roast).where(Roast.id == roast_id)).first()
    if not db_roast:
        raise HTTPException(status_code=404, detail=RESPONSE_404)
    
    update_model(db_roast, roast, session)
    session.add(db_roast)
    session.commit()
    session.refresh(db_roast)
    return db_roast

@router.delete("/{roast_id}", response_model=RESPONSE_404)
def delete_roast(roast_id: int, session: Session = Depends(get_session)) -> None:
    roast = session.exec(select(Roast).where(Roast.id == roast_id)).first()
    if not roast:
        raise HTTPException(status_code=404, detail=RESPONSE_404)
    
    session.delete(roast)
    session.commit()
    return DELETE_OK