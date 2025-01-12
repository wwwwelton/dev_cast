from typing import List

from pydantic import BaseModel


class DestinationBase(BaseModel):
    pass


class DestinationCreate(BaseModel):
    stream_key: str
    dest_name: str
    dest_url: str


class DestinationUpdate(BaseModel):
    pass


class Destination(DestinationBase):
    id: int
    stream_id: int
    stream_key: str
    pid: int
    dest_name: str
    dest_url: str
    live: bool

    class Config:
        from_attributes = True


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
