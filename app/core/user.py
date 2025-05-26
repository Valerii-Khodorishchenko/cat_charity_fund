from typing import Union

from fastapi import Depends
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
            self,
            password: str,
            user: Union[UserCreate, User]
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Пароль должен содержать не менее 3 символов.'
            )


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=BearerTransport(tokenUrl='auth/jwt/login'),
    get_strategy=lambda: JWTStrategy(
        secret=settings.secret,
        lifetime_seconds=3600
    )
)
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
