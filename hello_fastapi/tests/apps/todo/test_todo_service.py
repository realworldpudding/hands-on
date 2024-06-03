import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from pudding_todo.apps.account.models import User
from pudding_todo.apps.todo.models import Todo, TodoGroup
from pudding_todo.apps.todo.schemas import TodoCreateSchema, TodoGroupCreateSchema
from pudding_todo.apps.todo.services import TodoService, TodoGroupService


@pytest.fixture()
def todo_service(db_session: AsyncSession) -> TodoService:
    return TodoService(db_session)


@pytest.fixture()
async def todo_group(db_session: AsyncSession, valid_user: User) -> TodoGroup:
    service = TodoGroupService(db_session)
    payload = TodoGroupCreateSchema.model_validate({
        "name": "Test Group",
    })
    group = await service.create(valid_user.id, payload)
    return group


@pytest.fixture()
def payload(todo_group: TodoGroup) -> TodoCreateSchema:
    return TodoCreateSchema.model_validate({
        "name": "Test Todo",
        "group_id": todo_group.id,
    })

 

async def test_create(payload: TodoCreateSchema, todo_service: TodoService, valid_user: User):
    todo = await todo_service.create(valid_user.id, payload)
    
    assert isinstance(todo, Todo)
    assert todo.name == payload.name
    assert todo.user.id == valid_user.id
