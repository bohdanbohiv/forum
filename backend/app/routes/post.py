from http import HTTPStatus

from fastapi import APIRouter, Response, HTTPException
from sqlmodel import select

from ..db import SessionDep
from ..models import Post, PostCreate, PostPublic, PostUpdate
from ..utils import CurrentUser

router = APIRouter(prefix='/posts', tags=['posts'])


@router.post('/', response_model=PostPublic, status_code=HTTPStatus.CREATED)
def create_post(post: PostCreate, session: SessionDep,
                current_user: CurrentUser) -> Post:
    db_post = Post.model_validate(post, update={'owner_id': current_user.id})
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.get('/', response_model=list[PostPublic])
def read_posts(session: SessionDep, skip: int = 0, limit: int = 100
               ) -> list[Post]:
    return session.exec(select(Post).offset(skip).limit(limit)).all()


@router.get('/{post_id}', response_model=PostPublic)
def read_post(post_id: int, session: SessionDep) -> Post:
    post = session.get(Post, post_id)
    if post is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Post not found')
    return post


@router.patch('/{post_id}', response_model=PostPublic)
def update_post(post_id: int, post: PostUpdate, session: SessionDep,
                current_user: CurrentUser) -> Post:
    existing_post = session.get(Post, post_id)
    if existing_post is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Post not found')
    if existing_post.owner_id != current_user.id:
        raise HTTPException(HTTPStatus.UNAUTHORIZED,
                            'You are not the owner of the post')
    update_data = post.model_dump(exclude_unset=True)
    existing_post.sqlmodel_update(update_data)
    session.add(existing_post)
    session.commit()
    session.refresh(existing_post)
    return existing_post


@router.delete('/{post_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_post(post_id: int, session: SessionDep,
                current_user: CurrentUser) -> Response:
    post = session.get(Post, post_id)
    if post is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Post not found')
    if post.owner_id != current_user.id:
        raise HTTPException(HTTPStatus.UNAUTHORIZED,
                            'You are not the owner of the post')
    session.delete(post)
    session.commit()
    return Response(status_code=HTTPStatus.NO_CONTENT)
