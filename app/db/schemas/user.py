from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: Optional[str] = None
    is_active: Optional[bool] = False
    is_superuser: Optional[bool] = False


class UserBaseInDB(UserBase):
    id: int = None

    class Config:
        orm_mode = True


class UserCreate(UserBaseInDB):
    email: str
    password: str


class UserUpdate(UserBaseInDB):
    password: Optional[str] = None


class User(UserBaseInDB):
    pass


class UserInDB(UserBaseInDB):
    hashed_password: str