from pydantic import BaseModel


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

    class Config:
        from_attributes = True
