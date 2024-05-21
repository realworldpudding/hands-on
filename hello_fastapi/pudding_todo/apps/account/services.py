from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from starlette.authentication import UnauthenticatedUser
from fastapi_users import InvalidPasswordException
from pudding_todo.authentication import UserManagerDep
from pudding_todo.db import DbSessionDep

from .models import User

class UserService:
    _data = {
        "puddingcamp": "PuddingCamp2024",
    }
    session: AsyncSession

    def __init__(self, session: DbSessionDep, user_manager: UserManagerDep):
        self.session = session
        self.user_manager = user_manager

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)            
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def authenticate(self, username: str, password: SecretStr | str) -> User | UnauthenticatedUser:
        if isinstance(password, SecretStr):
            password = password.get_secret_value()

        user = await self.get_by_username(username)
        try:
            self.user_manager.validate_password(password, user)
        except InvalidPasswordException:
            return UnauthenticatedUser()

        return user

