from datetime import date
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, validator

from app.db.schemas.bike import BikeInDB


class OrderBase(BaseModel):
    bike_number: str
    date_begin: date
    date_end: date

    @validator('date_end')
    def date_end_must_be_greater_than_date_start(cls, v, values):
        if v <= values['date_begin']:
            raise ValueError(
                'date_end must be greater than date_start'
                )
        return v


class OrderCreate(OrderBase):
    date_begin: date
    date_end: date


class OrderInDB(OrderBase):
    uuid: UUID
    status: Enum
    user_id: int


class OrderResponse(OrderInDB):
    bike: BikeInDB

    class Config:
        orm_mode = True
