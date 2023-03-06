from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends


from app.db.crud.order import OrderCrud
from app.db.crud.bike import BikeCrud
from app.db.schemas.order import OrderCreate, OrderInDB, OrderResponse
from app.db.models.user import User
from app.api.utils.security import get_current_active_user

router = APIRouter()


@router.post('', response_model=OrderInDB)
async def create_order(
    order: OrderCreate,
    crud: OrderCrud = Depends(),
    user: User = Depends(get_current_active_user),
    bike_crud: BikeCrud = Depends()
):
    result = await crud.create_order(order, user, bike_crud)
    return result.__dict__


@router.get('', response_model=list[OrderResponse])
async def get_orders(
    status: str | None = None,
    crud: OrderCrud = Depends(),

):
    result = await crud.get_orders(status)
    return result


@router.patch('/update/{id}')
async def update_order(
    order_uuid: UUID,
    order: OrderCreate,
    crud: OrderCrud = Depends()
):
    result = await crud.update_order(order_uuid, order)
    if result:
        return result
    raise HTTPException(400, 'Order does not found')
