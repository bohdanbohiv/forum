from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import create_db_and_tables
from .routes import login, post, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
origins = ["http://localhost:5173"]  # Replace with the actual origin of your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Adjust to the allowed HTTP methods
    allow_headers=["*"],  # Adjust to the allowed headers
)
app.include_router(login.router)
app.include_router(post.router)
app.include_router(user.router)


@app.get('/')
def root():
    return {'message': 'Hello World'}
