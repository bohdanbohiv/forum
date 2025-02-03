from http import HTTPStatus

from fastapi import APIRouter, Response, HTTPException
from sqlmodel import select

from ..db import SessionDep
from ..models import *

router = APIRouter(prefix='/posts', tags=['posts'])


@router.post('/', response_model=PostPublic, status_code=HTTPStatus.CREATED)
def create_post(post: PostCreate, session: SessionDep) -> Post:
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.get('/', response_model=list[PostPublic])
def read_posts(session: SessionDep) -> list[Post]:
    return session.exec(select(Post)).all()


@router.get('/{post_id}', response_model=PostPublic)
def read_post(post_id: int, session: SessionDep) -> Post:
    post = session.get(Post, post_id)
    if post is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Post not found')
    return post


@router.patch('/{post_id}', response_model=PostPublic)
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


@router.delete('/{post_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_post(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)
    if post is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Post not found')
    session.delete(post)
    session.commit()
    return Response(status_code=HTTPStatus.NO_CONTENT)
