from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from ..db import SessionDep
from ..models import Token, User
from ..utils import pwd_context, create_access_token

router = APIRouter(tags=['login'])


@router.post('/login/access-token', response_model=Token)
def login_access_token(session: SessionDep,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = session.exec(
        select(User).where(User.email == form_data.username)).first()
    if user is None or not pwd_context.verify(form_data.password,
                                              user.hashed_password):
        raise HTTPException(HTTPStatus.UNAUTHORIZED,
                            'Incorrect email or password')
    return Token(access_token=create_access_token(user.id))
