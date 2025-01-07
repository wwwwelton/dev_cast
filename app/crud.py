import uuid

from sqlalchemy.orm import Session

from app.models import Item, Stream
from app.schemas import ItemCreate, StreamCreate


def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


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
