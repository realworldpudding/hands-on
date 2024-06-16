import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from pudding_todo.apps.account.models import User
from pudding_todo.apps.todo.models import Todo, TodoGroup
from pudding_todo.apps.todo.schemas import TodoCreateSchema, TodoGroupCreateSchema
from pudding_todo.apps.todo.services import TodoService, TodoGroupService


@pytest.fixture()
def todo_group_service(db_session: AsyncSession) -> TodoService:
    return TodoGroupService(db_session)


@pytest.fixture()
def todo_service(db_session: AsyncSession) -> TodoService:
    return TodoService(db_session)


@pytest.fixture()
async def todo_group(todo_group_service: TodoGroupService, valid_user: User) -> TodoGroup:
    payload = TodoGroupCreateSchema.model_validate({
        "name": "Test Group",
    })
    group = await todo_group_service.create(valid_user.id, payload)
    return group


@pytest.fixture()
async def todo_group2(todo_group_service: TodoGroupService, valid_user: User) -> TodoGroup:
    payload = TodoGroupCreateSchema.model_validate({
        "name": "Test Group 2"[::-1],
    })
    group = await todo_group_service.create(valid_user.id, payload)
    return group

