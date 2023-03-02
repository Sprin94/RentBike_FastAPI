from fastapi import APIRouter, Depends, HTTPException, status

from app.api.utils.security import get_current_active_user
from app.db.schemas.user import UserCreate
from app.db.crud.user import UserCrud
from app.db.schemas.user import UserBaseInDB
from app.db.models.user import User

router = APIRouter()


@router.post('', response_model=UserBaseInDB)
async def user_create(user: UserCreate,
                      crud: UserCrud = Depends()):
    result = await crud.create_user(user)
    return result


@router.get('/me', response_model=UserBaseInDB)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user
