from sqlmodel import Session

from .db import engine, init_db


def init() -> None:
    with Session(engine) as session:
        init_db(session)


if __name__ == '__main__':
    init()
