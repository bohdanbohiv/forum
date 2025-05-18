from http import HTTPStatus

from fastapi import APIRouter, Response, HTTPException
from sqlmodel import select

from ..deps import CurrentUser, SessionDep
from ..models import Post, Vote, VoteCast

router = APIRouter(prefix='/vote', tags=['vote'])


@router.post('/')
def cast_vote(vote: VoteCast, session: SessionDep,
              current_user: CurrentUser) -> Response:
    if session.get(Post, vote.post_id) is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Post not found')
    existing_vote = session.exec(
        select(Vote).where(Vote.post_id == vote.post_id,
                           Vote.user_id == current_user.id)).first()
    if vote.direction == 1:
        if existing_vote is not None:
            raise HTTPException(HTTPStatus.CONFLICT, 'Already voted')
        db_vote = Vote(post_id=vote.post_id, user_id=current_user.id)
        session.add(db_vote)
        session.commit()
        return Response(status_code=HTTPStatus.CREATED)
    if vote.direction == 0:
        if existing_vote is None:
            raise HTTPException(HTTPStatus.NOT_FOUND, 'Not voted')
        session.delete(existing_vote)
        session.commit()
        return Response(status_code=HTTPStatus.NO_CONTENT)
    raise HTTPException(HTTPStatus.BAD_REQUEST, 'Invalid vote direction')
