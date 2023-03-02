from datetime import timedelta

from fastapi import APIRouter, Form, HTTPException, status, Depends

from app.core.config import settings
from app.core.jwt import create_access_token
from app.db.schemas.token import Token
from app.db.crud.user import UserCrud
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
