from typing import AsyncGenerator, Annotated, Optional, Any

from sqlmodel import select

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, FastAPIUsers, InvalidPasswordException
from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.password import PasswordHelper
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from pudding_todo.db import DbSessionDep
from pudding_todo.apps.account.models import User

SECRET = "PuddingCamp"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


cookie_transport = CookieTransport(cookie_max_age=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

AuthBackendDep = Annotated[AuthenticationBackend[User, int], Depends(lambda: auth_backend)]


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def get(self, username: str | Any) -> Optional[User]:
        if isinstance(username, str):
            return await self.get_by_username(username)
        return await super().get(username)

    async def get_by_username(self, username: str) -> Optional[User]:
        statement = select(self.user_db.user_table).where(
            self.user_db.user_table.username == username,
        )
        return await self.user_db._get_user(statement)

    async def validate_password(self, password: str, user: User) -> None:
        result, _ = self.password_helper.verify_and_update(password, user.hashed_password)
        if not result:
            raise InvalidPasswordException("Password is incorrect.")

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def use_user_db(session: DbSessionDep) -> AsyncGenerator[SQLAlchemyUserDatabase[User, int], None]:
    yield SQLAlchemyUserDatabase(session, User)


UserDBDep = Annotated[SQLAlchemyUserDatabase[User, int], Depends(use_user_db)]

password_hash = PasswordHash((
    Argon2Hasher(),
))
password_helper = PasswordHelper(password_hash)

async def use_user_manager(user_db: UserDBDep) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db, password_helper)

UserManagerDep = Annotated[UserManager, Depends(use_user_manager)]

fastapi_users = FastAPIUsers[User, int](
    use_user_manager,
    [auth_backend],
)
