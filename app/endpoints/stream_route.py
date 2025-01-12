from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas import stream_schema
from app.services import stream_service

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/streams/{stream_key}", response_model=stream_schema.Stream)
def get_stream(stream_key: str, db: Session = Depends(get_db)):
    try:
        return stream_service.get_stream(db, stream_key)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/streams/", response_model=list[stream_schema.Stream])
def get_streams(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return stream_service.get_streams(db, skip=skip, limit=limit)


@router.post("/streams/", response_model=stream_schema.Stream)
def create_stream(stream: stream_schema.StreamCreate, db: Session = Depends(get_db)):
    return stream_service.create_stream(db, stream)


@router.patch("/streams/{stream_key}", response_model=stream_schema.Stream)
def update_stream(
    stream_key: str,
    stream_data: stream_schema.StreamUpdate,
    db: Session = Depends(get_db),
):
    try:
        return stream_service.update_stream(db, stream_key, stream_data)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/streams/{stream_key}", response_model=stream_schema.Stream)
def delete_stream(stream_key: str, db: Session = Depends(get_db)):
    try:
        return stream_service.delete_stream(db, stream_key)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
