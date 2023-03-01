from fastapi import APIRouter, Depends
from app.db.schemas.user import UserCreate
from app.db.crud.user import UserCrud


router = APIRouter()


@router.post('')
async def user_create(user: UserCreate,
                      crud: UserCrud = Depends()):
    result = await crud.create_user(user)
    return result
