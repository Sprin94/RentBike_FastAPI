from fastapi import APIRouter, HTTPException, Depends


from app.db.crud.order import OrderCrud
from app.db.schemas.order import OrderCreate, OrderInDB
from app.db.models.user import User
from app.api.utils.security import get_current_active_user

router = APIRouter()


@router.post('', response_model=OrderInDB)
async def create_order(
    order: OrderCreate,
    crud: OrderCrud = Depends(),
    user: User = Depends(get_current_active_user)
):
    result = await crud.create_order(order, user)
    return result.__dict__
