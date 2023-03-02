from enum import Enum

from pydantic import BaseModel


class BikeModelBase(BaseModel):
    brand: str
    model: str
    engine_capacity: int


class BikeModelCreate(BikeModelBase):
    pass


class BikeModelInDB(BikeModelBase):
    id: int


class BikeBase(BaseModel):
    number: str
    model_id: int
    color: str
    born_year: int
    mileage: int = 0
    cost_per_day: int


class BikeCreate(BikeBase):
    pass

    class Config:
        orm_mode = True


class BikeInDB(BikeBase):
    photo: str | None = None
    status: Enum

    class Config:
        orm_mode = True