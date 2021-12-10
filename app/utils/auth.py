from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import password as passwd
from ..database import crud
from ..dependencies import get_settings, get_db


ALGORITHM = "HS256"

settings = get_settings()

user_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.root_path}/users/token/",
    scheme_name="User"
)


def authenticate_user(db: Session, username: str, password: str):
    user_db = crud.get_user_by_login(db=db, login=username)
    if not user_db:
        return False
    if not passwd.verify(password, user_db.password):
        return False
    return user_db


def create_user_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(
        minutes=settings.access_token_expire_minutes)
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(user_oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_db = crud.get_user_by_login(db=db, login=username)
    if user_db is None:
        raise credentials_exception
    return user_db
