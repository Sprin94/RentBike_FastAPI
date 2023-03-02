from datetime import date
from uuid import UUID
from enum import Enum

from pydantic import BaseModel


class OrderBase(BaseModel):
    bike_number: str
    date_begin: date
    date_end: date


class OrderCreate(OrderBase):
    pass


class OrderInDB(OrderBase):
    uuid: UUID
    status: Enum
    user_id: int
