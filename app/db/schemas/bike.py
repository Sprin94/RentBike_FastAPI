from enum import Enum
from typing import Optional

from fastapi import File, UploadFile

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
    photo: Optional[str] = None


class BikeCreate(BikeBase):
    pass

    class Config:
        orm_mode = True


class BikeUpdate(BaseModel):
    color: Optional[str] = None
    mileage: Optional[int] = None
    cost_per_day: Optional[int] = None
    photo: Optional[UploadFile] = File(None)

    class Config:
        orm_mode = True


class BikeInDB(BaseModel):
    number: str
    color: str
    born_year: int
    mileage: int
    cost_per_day: int
    model: str
    photo: Optional[UploadFile] = None

    class Config:
        orm_mode = True
