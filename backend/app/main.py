from http import HTTPStatus

import psycopg
from datetime import datetime
from fastapi import FastAPI, Response, HTTPException
from psycopg.rows import dict_row
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    body: str
    private: bool = False
    images: list | None = None
    created_at: datetime | None = None


conn = psycopg.connect(
    '',
    row_factory=dict_row)
cur = conn.cursor()


@app.get('/')
def root():
    return {'message': 'Hello World'}


@app.post('/posts', status_code=HTTPStatus.CREATED)
def create_post(post: Post):
    cur.execute(
        'INSERT INTO posts (body, private) VALUES (%s, %s) RETURNING *',
        (post.body, post.private))
    new_post = cur.fetchone()
    conn.commit()
    return {'data': new_post}


@app.get('/posts')
def read_posts():
    cur.execute('SELECT * FROM posts')
    posts = cur.fetchall()
    return {'data': posts}


@app.get('/posts/{post_id}')
def read_post(post_id: int):
    cur.execute('SELECT * FROM posts WHERE id = %s', (post_id,))
    post = cur.fetchone()
    if post is None:
        raise HTTPException(HTTPStatus.NOT_FOUND,
                            f'Post with id {post_id} was not found')
    return {'post': post}


@app.put('/posts/{post_id}')
def update_post(post_id: int, post: Post):
    cur.execute('UPDATE posts SET private = %s WHERE id = %s RETURNING *',
                (post.private, post_id))
    updated_post = cur.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(HTTPStatus.NOT_FOUND,
                            f'Post with id {post_id} was not found')
    return {'data': updated_post}


@app.delete('/posts/{post_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_post(post_id: int):
    cur.execute('DELETE FROM posts WHERE id = %s RETURNING *', (post_id,))
    deleted_post = cur.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(HTTPStatus.NOT_FOUND,
                            f'Post with id {post_id} was not found')
    return Response(status_code=HTTPStatus.NO_CONTENT)
