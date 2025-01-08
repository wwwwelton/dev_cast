import uuid

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.models import Item, Stream
from app.schemas import ItemCreate, StreamCreate, StreamUpdate


def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


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
