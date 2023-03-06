from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from app.core.security import get_password_hash, verify_password
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

    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> bool | User:
        user = await self.get_by_email(email=email)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    async def update_user(
            self,
            email: str,
            data: dict
    ):
        password = data.get('password')
        if password:
            data.pop('password')
            data['hashed_password'] = get_password_hash(password)
        stmt = (update(User)
                .where(User.email == email)
                .values(**data)
                .returning(User)
                )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar()
        except IntegrityError:
            return False

    async def delete_user(self,
                          user_id: int):
        model = await self.session.get(User, user_id)
        if model:
            self.session.delete(model)
            await self.session.commit()
            return True
        raise HTTPException(status_code=404, detail="User not found.")
