from pudding_todo.db import DbSessionDep
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Todo
from .schemas import TodoCreateSchema

class TodoService:
    session: AsyncSession

    def __init__(self, session: DbSessionDep):
        self.session = session

    async def create(self, user_id: int, payload: TodoCreateSchema) -> Todo:
        todo = Todo(user_id=user_id, **payload.model_dump(mode="python"))
        self.session.add(todo)
        await self.session.commit()
        return todo

