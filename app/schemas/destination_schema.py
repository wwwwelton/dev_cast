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
