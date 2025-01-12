import uuid

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.models.stream_model import Stream
from app.schemas.stream_schema import StreamCreate, StreamUpdate


def get_stream(db: Session, stream_key: str):
    return db.query(Stream).filter(Stream.stream_key == stream_key).first()


def get_streams(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Stream).offset(skip).limit(limit).all()


def create_stream(db: Session, stream: StreamCreate):
    db_stream = Stream(
        stream_key=str(uuid.uuid4().hex),
        stream_name=stream.stream_name,
        live=False,
    )
    db.add(db_stream)
    db.commit()
    db.refresh(db_stream)
    return db_stream


def update_stream(db: Session, stream_key: str, stream_data: StreamUpdate):
    db_stream = get_stream(db, stream_key)
    if not db_stream:
        raise NoResultFound(f"Stream with stream_key {stream_key} not found")
    db_stream.live = stream_data.live
    db.commit()
    db.refresh(db_stream)
    return db_stream


def delete_stream(db: Session, stream_key: str):
    db_stream = get_stream(db, stream_key)
    if not db_stream:
        raise NoResultFound(f"Stream with stream_key {stream_key} not found")
    db.delete(db_stream)
    db.commit()
    return db_stream
