from sqlmodel import Session, create_engine, select

from .config import settings
from .models import User
from .security import pwd_context

engine = create_engine(settings.db_url)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
