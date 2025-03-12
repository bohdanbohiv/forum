from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import login, post, user, vote

app = FastAPI()
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(login.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)


@app.get('/')
def root():
    return {'message': 'Hello World'}
