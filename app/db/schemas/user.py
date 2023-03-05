from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: Optional[str]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserBaseInDB(UserBase):
    id: int = None
    name: str
    surname: str
    birth_day: Optional[date]

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    surname: str


class UserUpdate(BaseModel):
    password: str = None
    name: str = None
    surname: str = None
    birth_day: date = None


class User(UserBaseInDB):
    pass


class UserInDB(UserBaseInDB):
    hashed_password: str
