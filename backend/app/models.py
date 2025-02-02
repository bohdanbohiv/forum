from datetime import datetime

from pydantic import EmailStr
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


class UserBase(SQLModel):
    # profile_picture | None
    name: str = Field(max_length=255)


class UserCreate(UserBase):
    # profile_picture | None = None
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)


class UserPublic(UserBase):
    id: int
    created_at: datetime
