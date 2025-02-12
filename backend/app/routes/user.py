from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..db import SessionDep
from ..models import User, UserCreate, UserPublic
from ..utils import pwd_context

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate, session: SessionDep) -> User:
    if session.exec(
            select(User).where(User.email == user.email)).first() is not None:
        raise HTTPException(HTTPStatus.CONFLICT,
                            'The user with this email already exists')
    db_user = User.model_validate(user, update={
        'hashed_password': pwd_context.hash(user.password)})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get('/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'User not found')
    return user


@router.get('/', response_model=list[UserPublic])
def read_users(session: SessionDep, skip: int = 0, limit: int = 100,
               search: str = '') -> list[User]:
    statement = select(User)
    if search:
        statement = statement.where(User.name.contains(search))
    return session.exec(statement.offset(skip).limit(limit)).all()
