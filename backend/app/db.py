from sqlmodel import Session, create_engine, select

from .config import settings
from .models import User
from .security import pwd_context

engine = create_engine(settings.db_url)


def get_session():
    with Session(engine) as session:
        yield session


def init_db(session: Session) -> None:
    if session.exec(select(User).where(User.email == settings.first_su_email)
                    ).first() is None:
        db_user = User(
            name=settings.first_su_name,
            email=settings.first_su_email,
            hashed_password=pwd_context.hash(settings.first_su_password),
            is_superuser=True,
        )
        session.add(db_user)
        session.commit()
