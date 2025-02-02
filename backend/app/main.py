from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, Response, HTTPException
from passlib.context import CryptContext
from sqlmodel import select

from .db import create_db_and_tables, SessionDep
from .models import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@app.get('/')
def root():
    return {'message': 'Hello World'}


@app.post('/posts', response_model=PostPublic, status_code=HTTPStatus.CREATED)
def create_post(post: PostCreate, session: SessionDep) -> Post:
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@app.get('/posts', response_model=list[PostPublic])
def read_posts(session: SessionDep) -> list[Post]:
    return session.exec(select(Post)).all()


@app.get('/posts/{post_id}', response_model=PostPublic)
def read_post(post_id: int, session: SessionDep) -> Post:
    post = session.get(Post, post_id)
    if post is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Post not found')
    return post


@app.patch('/posts/{post_id}', response_model=PostPublic)
def update_post(post_id: int, post: PostUpdate, session: SessionDep):
    existing_post = session.get(Post, post_id)
    if existing_post is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Post not found')
    update_data = post.model_dump(exclude_unset=True)
    existing_post.sqlmodel_update(update_data)
    session.add(existing_post)
    session.commit()
    session.refresh(existing_post)
    return existing_post


@app.delete('/posts/{post_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_post(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)
    if post is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Post not found')
    session.delete(post)
    session.commit()
    return Response(status_code=HTTPStatus.NO_CONTENT)


@app.post('/users', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate, session: SessionDep) -> User:
    if session.exec(
            select(User).where(User.email == user.email)).first() is not None:
        raise HTTPException(
            HTTPStatus.CONFLICT,
            'The user with this email already exists in the system'
        )
    db_user = User.model_validate(user, update={
        'hashed_password': pwd_context.hash(user.password)})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
