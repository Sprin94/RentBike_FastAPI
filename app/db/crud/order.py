from sqlalchemy import select


from app.db.crud.base import BaseCrud
from app.db.models.order import Order
from app.db.models.user import User
from app.db.models import user, bike
from app.db.schemas.order import OrderCreate


class OrderCrud(BaseCrud):
    async def get_all_order(self) -> list[Order]:
        stmt = (select(Order).join(bike.Bike).join(user.User))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_order(self, order: OrderCreate, user: User) -> Order:
        order_dict = order.dict()
        order_dict['user_id'] = user.id
        order = Order(**order_dict)
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order
