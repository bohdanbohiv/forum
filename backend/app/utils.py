from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import ValidationError

from .config import settings
from .db import SessionDep
from .models import TokenData, User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2 = OAuth2PasswordBearer(tokenUrl='login/access-token')

ALGORITHM = 'HS256'


def create_access_token(subject) -> str:
    return jwt.encode({'exp': datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes), 'sub': str(subject)},
                      settings.secret_key, ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2)],
                     session: SessionDep) -> User:
    try:
        token_data = TokenData(**jwt.decode(token, settings.secret_key,
                                            algorithms=[ALGORITHM]))
    except (InvalidTokenError, ValidationError):
        raise HTTPException(HTTPStatus.UNAUTHORIZED, 'Invalid token',
                            {'WWW-Authenticate': 'Bearer'})
    user = session.get(User, int(token_data.sub))
    if not user:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'User not found')
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
