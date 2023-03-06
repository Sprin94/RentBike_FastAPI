from datetime import date
from typing import Optional
import re

from pydantic import BaseModel, validator


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

    @validator('password')
    def password_correct(cls, value):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)' \
                  r'(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'

        if value and re.match(pattern, value) is None:
            raise ValueError('Password has incorrect format.')
        return value


class UserUpdate(BaseModel):
    password: str = None
    name: str = None
    surname: str = None
    birth_day: date = None

    @validator('password')
    def password_correct(cls, value):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)' \
                  r'(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'

        if value and re.match(pattern, value) is None:
            raise ValueError('Password has incorrect format.')
        return value


class User(UserBaseInDB):
    pass


class UserInDB(UserBaseInDB):
    hashed_password: str
