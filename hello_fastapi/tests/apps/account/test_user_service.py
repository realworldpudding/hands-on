import pytest

from starlette.authentication import UnauthenticatedUser
from sqlalchemy.ext.asyncio import AsyncSession

from pudding_todo.apps.account.models import User, BaseUser
from pudding_todo.apps.account.services import UserService
from pudding_todo.authentication import UserManager


@pytest.fixture()
def user_service(db_session: AsyncSession, user_manager: UserManager) -> UserService:
    return UserService(db_session, user_manager)


@pytest.mark.parametrize(
    "username, password, expected, is_authenticated",
    [
        ("test", "password", UnauthenticatedUser, False),
        ("puddingcamp", "wrong", UnauthenticatedUser, False),
        ("puddingcamp", "PuddingCamp2024", User, True),
    ],
)
@pytest.mark.usefixtures("valid_user")
async def test_login(username, password, expected, is_authenticated, user_service):
    user = await user_service.authenticate(username, password)
    assert isinstance(user, BaseUser)
    assert isinstance(user, expected)
    assert user.is_authenticated is is_authenticated
