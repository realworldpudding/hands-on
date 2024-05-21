import pytest
from fastapi import status
from fastapi.testclient import TestClient

from pudding_todo.app import app


@pytest.mark.parametrize(
    "username, password, expected_status_code",
    [
        ("puddingcamp", "wrongwrong", status.HTTP_401_UNAUTHORIZED),
        ("puddingcamp", "wrong", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("puddingcamp", None, status.HTTP_422_UNPROCESSABLE_ENTITY),
        (None, "wrongwrong", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
def test_failed_login(username: str, password: str, expected_status_code: int, client: TestClient):
    payload = {"username": username, "password": password}
    res = client.post(app.router.url_path_for("login"), json=payload)
    assert res.status_code == expected_status_code


def test_login_successfully(client: TestClient):
    payload = {"username": "puddingcamp", "password": "PuddingCamp2024"}
    res = client.post(app.router.url_path_for("login"), json=payload)
    assert res.status_code == status.HTTP_200_OK

