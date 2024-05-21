import pytest

from starlette.authentication import UnauthenticatedUser
from pudding_todo.apps.account.models import User, BaseUser
from pudding_todo.apps.account.services import UserService


@pytest.fixture()
def user_service() -> UserService:
    return UserService()


@pytest.mark.parametrize(
    "username, password, expected, is_authenticated",
    [
        ("test", "password", UnauthenticatedUser, False),
        ("puddingcamp", "wrong", UnauthenticatedUser, False),
        ("puddingcamp", "PuddingCamp2024", User, True),
    ],
)
async def test_login(username, password, expected, is_authenticated, user_service):
    user = await user_service.authenticate(username, password)
    assert isinstance(user, BaseUser)
    assert isinstance(user, expected)
    assert user.is_authenticated is is_authenticated
