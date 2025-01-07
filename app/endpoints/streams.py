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


@router.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_items(db, skip=skip, limit=limit)


@router.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)


@router.get("/streams", response_model=list[schemas.Stream])
def read_streams(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_streams(db, skip=skip, limit=limit)


@router.post("/streams", response_model=schemas.Stream)
def create_stream(stream: schemas.StreamCreate, db: Session = Depends(get_db)):
    return crud.create_stream(db, stream)
