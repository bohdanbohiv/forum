from datetime import datetime, timezone, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2 = OAuth2PasswordBearer(tokenUrl='login/access-token')
ALGORITHM = 'HS256'


def create_access_token(subject) -> str:
    return jwt.encode({'exp': datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes), 'sub': str(subject)},
                      settings.secret_key, ALGORITHM)
