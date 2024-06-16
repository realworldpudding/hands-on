import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from pudding_todo.apps.account.models import User
from pudding_todo.apps.todo.models import TodoGroup
from pudding_todo.apps.todo.schemas import TodoGroupCreateSchema
from pudding_todo.apps.todo.services import TodoGroupService
from pudding_todo.exceptions import DuplicatedError


@pytest.fixture()
def todo_group_service(db_session: AsyncSession) -> TodoGroupService:
    return TodoGroupService(db_session)


@pytest.fixture()
def payload() -> TodoGroupCreateSchema:
    return TodoGroupCreateSchema(name="Test Group")


async def test_create(payload: TodoGroupCreateSchema, todo_group_service: TodoGroupService, valid_user: User):
    todo_group = await todo_group_service.create(valid_user.id, payload)

    assert isinstance(todo_group, TodoGroup)
    assert todo_group.name == payload.name
    assert todo_group.user.id == valid_user.id


async def test_cannot_create_duplicated_name(payload: TodoGroupCreateSchema, todo_group_service: TodoGroupService, valid_user: User):
    await todo_group_service.create(valid_user.id, payload)
    with pytest.raises(DuplicatedError):
        await todo_group_service.create(valid_user.id, payload)


async def test_findall_by_user_id(
        payload: TodoGroupCreateSchema,
        todo_group_service: TodoGroupService,
        valid_user: User,
        valid_user2: User,
    ) -> None:
    todo_group1 = await todo_group_service.create(valid_user.id, payload)
    todo_group2 = await todo_group_service.create(valid_user2.id, payload)

    groups = await todo_group_service.findall(valid_user.id)
    id_set = frozenset(group.id for group in groups)

    assert len(groups) == 1
    assert todo_group1.id in id_set
    assert todo_group2.id not in id_set
