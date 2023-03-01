from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.security import get_password_hash
from app.db.crud.base import BaseCrud
from app.db.models.user import User
from app.db.schemas.user import UserCreate


class UserCrud(BaseCrud):
    async def get_by_email(self, email: str):
        stmt = (select(User).where(User.email == email))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user: UserCreate):
        new_user_data = user.dict()
        password = new_user_data.pop('password')
        new_user_data["hashed_password"] = get_password_hash(password)
        user = User(**new_user_data)
        self.session.add(user)
        try:
            await self.session.commit()
            await self.session.refresh(user)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="User already exist.")
        return user
