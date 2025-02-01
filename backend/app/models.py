from datetime import datetime

from sqlmodel import Field, SQLModel

POST_BODY_MAX_LEN = 280


class PostBase(SQLModel):
    private: bool = False


class Post(PostBase, table=True):
    # images: list | None = None
    id: int | None = Field(default=None, primary_key=True)
    body: str = Field(max_length=POST_BODY_MAX_LEN)
    created_at: datetime = Field(default_factory=datetime.now)


class PostPublic(PostBase):
    # images: list | None
    id: int
    body: str
    created_at: datetime


class PostCreate(PostBase):
    # images: list | None = None
    body: str = Field(max_length=POST_BODY_MAX_LEN)


class PostUpdate(PostBase):
    private: bool | None = None
