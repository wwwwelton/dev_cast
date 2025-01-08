from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/destinations/", response_model=schemas.Destination)
def create_destination(
    destination: schemas.DestinationCreate, db: Session = Depends(get_db)
):
    return crud.create_destination(db, destination)
