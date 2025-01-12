from typing import List

from pydantic import BaseModel

from app.schemas.destination_schema import Destination


class StreamBase(BaseModel):
    stream_name: str


class StreamCreate(StreamBase):
    pass


class StreamUpdate(BaseModel):
    live: bool


class Stream(StreamBase):
    id: int
    stream_key: str
    live: bool
    destinations: List[Destination] = []

    class Config:
        from_attributes = True
