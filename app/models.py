from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class Stream(Base):
    __tablename__ = "stream"
    id = Column(Integer, primary_key=True, index=True)
    stream_key = Column(String(36), unique=True, index=True)
    stream_name = Column(String)
    live = Column(Boolean, default=False)
