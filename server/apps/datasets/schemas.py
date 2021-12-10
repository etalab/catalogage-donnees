from pydantic import BaseModel


class DatasetBase(BaseModel):
    name: str


class DatasetCreate(DatasetBase):
    pass


class Dataset(DatasetBase):
    id: int

    class Config:
        orm_mode = True
