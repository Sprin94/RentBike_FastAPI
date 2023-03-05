from pydantic import BaseModel

from app.db.schemas.user import UserBaseInDB


class ResponseSignUp(BaseModel):
    user: UserBaseInDB
    message: str
