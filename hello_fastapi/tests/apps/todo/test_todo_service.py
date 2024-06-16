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


@pytest.fixture()
async def todos(
        todo_group: TodoGroup,
        todo_group2: TodoGroup,
        todo_service: TodoService,
    ):
    result = []
    for group in [todo_group, todo_group2]:
        for i in range(1, 3):
            payload = TodoCreateSchema.model_validate({
                "name": f"Test Todo {i} for {group.name}",
                "group_id": group.id,
            })
            todo = await todo_service.create(payload)
            result.append(todo)
    return result


@pytest.fixture()
def payload(todo_group: TodoGroup) -> TodoCreateSchema:
    return TodoCreateSchema.model_validate({
        "name": "Test Todo",
        "group_id": todo_group.id,
    })

 

async def test_create(payload: TodoCreateSchema, todo_service: TodoService, valid_user: User):
    todo = await todo_service.create(payload)
    
    assert isinstance(todo, Todo)
    assert todo.name == payload.name
    assert todo.group.user.id == valid_user.id


@pytest.mark.usefixtures("todos")
async def test_findall_by_group_id(
        todo_group: TodoGroup,
        todo_service: TodoService,
        todo_group_service: TodoGroupService,
        valid_user: User,
    ):
    service = todo_service
    group = await todo_group_service.get_by_id(todo_group.id)
    id_set = frozenset([todo.id for todo in group.todos])

    todos = await service.findall(valid_user.id, group_id=todo_group.id)
    expected_id_set = frozenset([todo.id for todo in todos])

    assert all(todo.group.id == todo_group.id for todo in todos)
    assert expected_id_set
    assert id_set == expected_id_set
