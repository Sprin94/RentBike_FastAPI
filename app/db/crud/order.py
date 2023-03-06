from uuid import UUID

from fastapi import HTTPException, Depends
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.db.crud.base import BaseCrud
from app.db.crud.bike import BikeCrud
from app.db.models.order import Order
from app.db.models.user import User
from app.db.schemas.order import OrderCreate


class OrderCrud(BaseCrud):
    async def get_orders(self, status: str | None) -> list[Order]:
        stmt = (select(Order)
                .options(joinedload(Order.bike))
                )
        if status:
            stmt = stmt.where(Order.status == status)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_order(self, order: OrderCreate, user: User,
                           bike_crud: BikeCrud) -> Order:
        order_dict = order.dict()
        order_dict['user_id'] = user.id
        order = Order(**order_dict)
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order
        raise HTTPException(status_code=400, detail="No bikes available")

    async def update_order(self, uuid: UUID, order: OrderCreate):
        stmt = (update(Order)
                .where(Order.uuid == uuid)
                .values(**order.dict())
                .returning(Order))
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            await self.session.refresh(result)
            return result
        except UnmappedInstanceError:
            return False
