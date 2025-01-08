import uuid

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.models import Destination, Stream
from app.schemas import DestinationCreate, StreamCreate, StreamUpdate


def get_stream(db: Session, stream_key: str):
    db_stream = db.query(Stream).filter(Stream.stream_key == stream_key).first()
    if not db_stream:
        raise NoResultFound(f"Stream with stream_key {stream_key} not found")
    return db_stream


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
    db_stream.live = stream_data.live
    db.commit()
    db.refresh(db_stream)
    return db_stream


def delete_stream(db: Session, stream_key: str):
    db_stream = get_stream(db, stream_key)
    db.delete(db_stream)
    db.commit()
    return db_stream


def create_destination(
    db: Session,
    destination: DestinationCreate,
):
    db_stream = get_stream(db, destination.stream_key)
    db_dest = Destination(
        stream_id=db_stream.id,
        stream_key=db_stream.stream_key,
        dest_name=destination.dest_name,
        dest_url=destination.dest_url,
    )
    db.add(db_dest)
    db.commit()
    db.refresh(db_dest)
    return db_dest
