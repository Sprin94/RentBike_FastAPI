from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.db.crud.user import UserCrud
from app.core.jwt import ALGORITHM
from app.core.config import settings
from app.db.schemas.token import TokenData
from app.db.schemas.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        crud: UserCrud = Depends(),
        ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,
                             settings.SECRET_KEY,
                             algorithms=[ALGORITHM]
                             )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await crud.get_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
        current_user: User = Depends(get_current_active_user),
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
