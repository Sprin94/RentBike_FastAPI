from fastapi import APIRouter, Depends, HTTPException, status

from app.api.utils.security import (get_current_active_user,
                                    get_current_active_superuser)
from app.db.schemas.user import UserCreate, UserUpdate
from app.db.crud.user import UserCrud
from app.db.schemas.user import UserBaseInDB
from app.db.models.user import User

router = APIRouter()


@router.post('', response_model=UserBaseInDB)
async def user_create(user: UserCreate,
                      crud: UserCrud = Depends(),
                      admin: User = Depends(get_current_active_superuser)):
    result = await crud.create_user(user)
    return result


@router.delete('/{user_id}')
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_active_superuser),
    crud: UserCrud = Depends()
):
    await crud.delete_user(user_id)
    return {'detail': 'User deleted'}


@router.get('/me', response_model=UserBaseInDB)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.patch('/me', response_model=UserBaseInDB)
async def update_me(
        data: UserUpdate,
        current_user: User = Depends(get_current_active_user),
        crud: UserCrud = Depends()):

    user = await crud.update_user(
        email=current_user.email,
        data=data)
    return user
