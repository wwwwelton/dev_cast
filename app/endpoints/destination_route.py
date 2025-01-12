from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas import destination_schema
from app.services import destination_service

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/destinations/", response_model=destination_schema.Destination)
def create_destination(
    destination: destination_schema.DestinationCreate, db: Session = Depends(get_db)
):
    return destination_service.create_destination(db, destination)