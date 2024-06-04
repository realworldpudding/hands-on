import pytest

from fastapi import status
from fastapi.testclient import TestClient

from sqlalchemy.ext.asyncio import AsyncSession

from pudding_todo.app import app
from pudding_todo.apps.account.models import User
from pudding_todo.apps.todo.models import TodoGroup
from pudding_todo.apps.todo.schemas import TodoCreateSchema, TodoGroupCreateSchema
from pudding_todo.apps.todo.services import TodoGroupService
from pudding_todo.authentication import auth_backend
from tests.apps.todo.test_todo_group_service import todo_group_service


@pytest.fixture()
async def todo_group(db_session: AsyncSession, valid_user: User) -> TodoGroup:
    service = TodoGroupService(db_session)
    payload = TodoGroupCreateSchema.model_validate({
        "name": "Test Group",
    })
    group = await service.create(valid_user.id, payload)
    return group


@pytest.fixture()
async def todo_group2(db_session: AsyncSession, valid_user2: User) -> TodoGroup:
    service = TodoGroupService(db_session)
    payload = TodoGroupCreateSchema.model_validate({
        "name": "Test Group",
    })
    group = await service.create(valid_user2.id, payload)
    return group



@pytest.fixture()
def payload(todo_group: TodoGroup) -> dict:
    schema = TodoCreateSchema.model_validate({
        "name": "Test Todo",
        "group_id": todo_group.id,
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
    assert data["group_id"] == payload["group_id"]


async def test_cannot_create_todo_without_auth(payload: dict, client: TestClient):
    url = app.router.url_path_for("create-todo")

    res = client.post(url, json=payload)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


async def test_cannot_create_todo_with_others_group(
    payload: dict,
    client: TestClient,
    todo_group2: TodoGroup,
    valid_user: User,
):
    payload["group_id"] = todo_group2.id
    url = app.router.url_path_for("create-todo")
    token = await auth_backend.get_strategy().write_token(valid_user)
    cookies = {auth_backend.transport.cookie_name: token}

    res = client.post(url, json=payload, cookies=cookies)
    assert res.status_code == status.HTTP_404_NOT_FOUND
