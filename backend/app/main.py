from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import create_db_and_tables
from .routes import login, post, user, vote


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(login.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)


@app.get('/')
def root():
    return {'message': 'Hello World'}
