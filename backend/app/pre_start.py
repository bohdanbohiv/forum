from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import retry, stop_after_attempt, wait_fixed

from .db import engine

max_tries = 60 * 5
wait_seconds = 1


@retry(stop=stop_after_attempt(max_tries), wait=wait_fixed(wait_seconds))
def init(db_engine: Engine) -> None:
    with Session(db_engine) as session:
        session.exec(select(1))


if __name__ == '__main__':
    init(engine)
