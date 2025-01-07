from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str
    price: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True


class StreamBase(BaseModel):
    stream_name: str


class StreamCreate(StreamBase):
    pass


class Stream(StreamBase):
    id: int
    stream_key: str
    live: bool

    class Config:
        from_attributes = True
