from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

POST_BODY_MAX_LEN = 280


class VoteBase(SQLModel):
    post_id: int


class VoteCast(VoteBase):
    direction: int = Field(ge=0, le=1)


class Vote(VoteBase, table=True):
    post_id: int | None = Field(default=None, foreign_key='post.id',
                                primary_key=True)
    user_id: int | None = Field(default=None, foreign_key='user.id',
                                primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)


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
    posts: list['Post'] = Relationship(back_populates='owner',
                                       cascade_delete=True)
    votes: list['Post'] = Relationship(back_populates='voters',
                                       link_model=Vote)


class UserPublic(UserBase):
    id: int
    created_at: datetime


class PostBase(SQLModel):
    private: bool = False


class Post(PostBase, table=True):
    # images: list | None = None
    id: int | None = Field(default=None, primary_key=True)
    body: str = Field(max_length=POST_BODY_MAX_LEN)
    created_at: datetime = Field(default_factory=datetime.now)
    owner_id: int = Field(foreign_key='user.id', nullable=False,
                          ondelete='CASCADE')
    owner: User | None = Relationship(back_populates='posts')
    voters: list[User] = Relationship(back_populates='votes', link_model=Vote)


class PostPublic(PostBase):
    # images: list | None
    id: int
    body: str
    created_at: datetime
    owner_id: int
    voters: list[UserPublic]


class PostCreate(PostBase):
    # images: list | None = None
    body: str = Field(max_length=POST_BODY_MAX_LEN)


class PostUpdate(PostBase):
    private: bool | None = None


class Token(SQLModel):
    access_token: str
    token_type: str = 'bearer'


class TokenData(SQLModel):
    sub: str | None = None
