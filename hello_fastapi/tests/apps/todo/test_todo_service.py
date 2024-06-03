import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from pudding_todo.apps.account.models import User
from pudding_todo.apps.todo.models import Todo
from pudding_todo.apps.todo.schemas import TodoCreateSchema
from pudding_todo.apps.todo.services import TodoService


@pytest.fixture()
def todo_service(db_session: AsyncSession) -> TodoService:
    return TodoService(db_session)


@pytest.fixture()
def payload(todo_group) -> TodoCreateSchema:
    return TodoCreateSchema.model_validate({
        "name": "Test Todo",
    })

 

async def test_create(payload: TodoCreateSchema, todo_service: TodoService, valid_user: User):
    todo = await todo_service.create(valid_user.id, payload)
    
    assert isinstance(todo, Todo)
    assert todo.name == payload.name
    assert todo.user.id == valid_user.id
