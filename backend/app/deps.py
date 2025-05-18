from http import HTTPStatus
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from .config import settings
from .db import get_session
from .models import TokenData, User
from .security import oauth2, ALGORITHM

SessionDep = Annotated[Session, Depends(get_session)]


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
