from pudding_todo.db import DbSessionDep
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from pudding_todo.exceptions import DuplicatedError
from .models import Todo, TodoGroup
from .schemas import TodoGroupCreateSchema, TodoCreateSchema

class TodoGroupService:
    session: AsyncSession

    def __init__(self, session: DbSessionDep):
        self.session = session

    async def create(self, user_id: int, payload: TodoGroupCreateSchema) -> TodoGroup:
        group = TodoGroup(user_id=user_id, **payload.model_dump(mode="python"))
        self.session.add(group)
        try:
            await self.session.commit()
        except IntegrityError as e:
            raise DuplicatedError(detail="이미 존재하는 그룹 이름입니다.") from e
        return group


class TodoService:
    session: AsyncSession

    def __init__(self, session: DbSessionDep):
        self.session = session

    async def create(self, user_id: int, payload: TodoCreateSchema) -> Todo:
        todo = Todo(user_id=user_id, **payload.model_dump(mode="python"))
        self.session.add(todo)
        await self.session.commit()
        return todo

