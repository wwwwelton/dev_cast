from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.models.destination_model import Destination
from app.schemas.destination_schema import DestinationCreate
from app.services.stream_service import get_stream


def create_destination(
    db: Session,
    destination: DestinationCreate,
):
    db_stream = get_stream(db, destination.stream_key)
    if not db_stream:
        raise NoResultFound(
            f"Stream with stream_key {destination.stream_key} not found"
        )
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
