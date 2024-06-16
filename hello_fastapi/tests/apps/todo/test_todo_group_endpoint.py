import pytest

from fastapi.testclient import TestClient

from pudding_todo.app import app
from pudding_todo.apps.account.models import User
from pudding_todo.apps.todo.endpoints import list_todo_group
from pudding_todo.apps.todo.services import TodoGroupService
from pudding_todo.authentication import auth_backend


@pytest.mark.usefixtures("todo_group", "todo_group2")
async def test_list_todo_group(
    valid_user: User,
    todo_group_service: TodoGroupService,
) -> None:

    result = await list_todo_group(valid_user, todo_group_service)

    assert "groups" in result
    assert len(result["groups"]) == 2


@pytest.mark.usefixtures("todo_group", "todo_group2")
async def test_list_todo_group_page(
    valid_user: User,
    client: TestClient,
) -> None:
    url = app.router.url_path_for("list-todo-group")
    token = await auth_backend.get_strategy().write_token(valid_user)
    cookies = {auth_backend.transport.cookie_name: token}

    res = client.get(url, cookies=cookies)
    data = res.json()
    assert "groups" in data
    assert len(data["groups"]) == 2

