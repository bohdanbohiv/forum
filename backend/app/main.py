from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import create_db_and_tables
from .routes import post, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(post.router)
app.include_router(user.router)


@app.get('/')
def root():
    return {'message': 'Hello World'}
