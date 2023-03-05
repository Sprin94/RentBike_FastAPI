from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import JWTError, jwt

from app.core.config import settings

ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
        )
    return encoded_jwt


def verify_token_for_activate(token: str) -> str:
    try:
        payload = jwt.decode(token,
                             settings.SECRET_KEY,
                             algorithms=[ALGORITHM]
                             )
        email = payload.get('email')
        if payload.get('status') == 'new' and email:
            return email
        raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
