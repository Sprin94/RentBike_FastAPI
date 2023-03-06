from datetime import timedelta

from fastapi import APIRouter, Form, HTTPException, status, Depends

from app.core.config import settings
from app.core.jwt import create_access_token, verify_token_for_activate
from app.db.schemas.token import Token
from app.db.schemas.user import UserCreate, UserBaseInDB
from app.db.crud.user import UserCrud
from app.tasks.tasks import task_send_mail_registration
from app.api.response_schemas import ResponseSignUp


router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    email: str = Form(),
    password: str = Form(),
    crud: UserCrud = Depends()
):
    user = await crud.authenticate_user(email=email, password=password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/sign-up", response_model=ResponseSignUp)
async def user_registration(
    user: UserCreate,
    crud: UserCrud = Depends()
):
    user = await crud.create_user(user)
    token = create_access_token({'email': user.email, 'status': 'new'})
    task_send_mail_registration.delay(
        user.email,
        token,
    )
    return {'user': user,
            'message': 'Confirm your mail'}


@router.get("/activation/{token}", response_model=UserBaseInDB)
async def user_activation(
    token: str,
    crud: UserCrud = Depends()
):
    email = verify_token_for_activate(token)
    user = await crud.update_user(email=email, data={'is_active': True})
    if user:
        return user
    raise HTTPException(400, 'User does not found')
