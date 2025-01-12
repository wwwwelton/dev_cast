from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Stream(Base):
    __tablename__ = "stream"
    id = Column(Integer, primary_key=True, index=True)
    stream_key = Column(String(36), unique=True, index=True)
    stream_name = Column(String)
    live = Column(Boolean, default=False)

    destinations = relationship(
        "Destination", back_populates="stream", cascade="all, delete-orphan"
    )


class Destination(Base):
    __tablename__ = "destination"
    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(Integer, ForeignKey("stream.id"))
    stream_key = Column(String(36), index=True)
    pid = Column(Integer, default=-1)
    dest_name = Column(String, index=True)
    dest_url = Column(String)
    live = Column(Boolean, default=False)

    stream = relationship("Stream", back_populates="destinations")
