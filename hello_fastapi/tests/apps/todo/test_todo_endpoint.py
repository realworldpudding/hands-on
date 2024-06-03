import pytest

from fastapi import status
from fastapi.testclient import TestClient

from pudding_todo.app import app
from pudding_todo.apps.account.models import User
from pudding_todo.apps.todo.schemas import TodoCreateSchema
from pudding_todo.authentication import auth_backend


@pytest.fixture()
def payload() -> dict:
    schema = TodoCreateSchema.model_validate({
        "name": "Test Todo",
    })
    return schema.model_dump(mode="json")


async def test_create_todo(payload: dict, client: TestClient, valid_user: User):
    url = app.router.url_path_for("create-todo")
    token = await auth_backend.get_strategy().write_token(valid_user)
    cookies = {auth_backend.transport.cookie_name: token}

    res = client.post(url, json=payload, cookies=cookies)
    assert res.status_code == status.HTTP_201_CREATED
    data = res.json()
    assert data["name"] == payload["name"]
    assert data["user_id"] == valid_user.id
