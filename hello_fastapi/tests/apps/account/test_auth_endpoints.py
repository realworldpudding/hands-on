import pytest
from fastapi import status
from fastapi.testclient import TestClient

from pudding_todo.app import app
from pudding_todo.apps.account.models import User
from pudding_todo.authentication import auth_backend

@pytest.mark.parametrize(
    "password, expected_status_code",
    [
        ("wrongwrong", status.HTTP_401_UNAUTHORIZED),
        ("wrong", status.HTTP_422_UNPROCESSABLE_ENTITY),
        (None, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
def test_failed_login(password: str, expected_status_code: int, client: TestClient, valid_user: User):
    payload = {"username": valid_user.username, "password": password}
    res = client.post(app.router.url_path_for("login"), json=payload)
    assert res.status_code == expected_status_code


def test_login_successfully(client: TestClient, valid_user: User):
    payload = {"username": valid_user.username, "password": "PuddingCamp2024"}
    res = client.post(app.router.url_path_for("login"), json=payload)
    assert res.status_code == status.HTTP_204_NO_CONTENT
    assert auth_backend.transport.cookie_name in res.cookies
    assert not not res.cookies[auth_backend.transport.cookie_name]
