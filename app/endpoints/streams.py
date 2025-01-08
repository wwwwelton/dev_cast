from fastapi import APIRouter, Depends, HTTPException
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


@router.get("/streams/{stream_key}", response_model=schemas.Stream)
def get_stream(stream_key: str, db: Session = Depends(get_db)):
    try:
        return crud.get_stream(db, stream_key)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/streams/", response_model=list[schemas.Stream])
def get_streams(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_streams(db, skip=skip, limit=limit)


@router.post("/streams/", response_model=schemas.Stream)
def create_stream(stream: schemas.StreamCreate, db: Session = Depends(get_db)):
    return crud.create_stream(db, stream)


@router.patch("/streams/{stream_key}", response_model=schemas.Stream)
def update_stream(
    stream_key: str, stream_data: schemas.StreamUpdate, db: Session = Depends(get_db)
):
    try:
        return crud.update_stream(db, stream_key, stream_data)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/streams/{stream_key}", response_model=schemas.Stream)
def delete_stream(stream_key: str, db: Session = Depends(get_db)):
    try:
        return crud.delete_stream(db, stream_key)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
