from datetime import datetime
from typing import Optional, Sequence

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlmodel import select, func

from pudding_todo.db import DbSessionDep
from pudding_todo.exceptions import DuplicatedError

from ...exceptions import PermissionDenidedError
from .models import Todo, TodoGroup, Attachment
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
    
    async def get_users_group_by_id(self, user_id: int, group_id: int) -> TodoGroup | None:
        stmt = select(TodoGroup).where(TodoGroup.user_id == user_id, TodoGroup.id == group_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, group_id: int) -> TodoGroup | None:
        stmt = select(TodoGroup).where(TodoGroup.id == group_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def findall(self, user_id: int) -> Sequence[TodoGroup]:
        stmt = select(TodoGroup).where(TodoGroup.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()


class TodoService:
    session: AsyncSession

    def __init__(self, session: DbSessionDep):
        self.session = session

    async def create(self, payload: TodoCreateSchema) -> Todo:
        todo = Todo(**payload.model_dump(mode="python"))
        self.session.add(todo)
        await self.session.commit()
        return todo

    async def findall(
            self,
            user_id: int,
            *,
            group_id: Optional[int] = None,
            offset: int = 0,
            limit: int = 10,
            is_completed: Optional[bool] = None,
        ) -> Sequence[Todo]:
        stmt = (
            select(Todo)
            .join(TodoGroup)
            .where(TodoGroup.user_id == user_id)
            .offset(offset)
            .limit(limit)
            .order_by(Todo.updated_at.desc())
        )

        if group_id:
            stmt = stmt.where(Todo.group_id == group_id)

        if is_completed is not None:
            stmt = stmt.where(Todo.is_completed.is_(is_completed))
        # 또는 다음과 같이 사용할 수도 있습니다.
        # if is_completed is True:
        #     stmt = stmt.where(Todo.is_completed)
        # elif is_completed is False:
        #     stmt = stmt.where(~Todo.is_completed)

        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def get_by_id(self, todo_id: int) -> Todo | None:
        stmt = select(Todo).where(Todo.id == todo_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def count_by_group_id(self, user_id: int, group_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(Todo)
            .where(Todo.group.has(TodoGroup.user_id == user_id))
            .where(Todo.group_id == group_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one() or 0
    
    async def set_completed_at(self, user_id: int, todo: Todo, when: Optional[datetime] = None) -> Todo:
        if todo.group.user_id != user_id:
            raise PermissionDenidedError()
        
        if when:
            todo.cancelled_at = None
        todo.completed_at = when
        self.session.add(todo)
        await self.session.commit()
        await self.session.refresh(todo)
        return todo


class AttachmentService: 
    session: AsyncSession

    def __init__(self, session: DbSessionDep):
        self.session = session

    async def create(self, todo_id: int, file: UploadFile) -> Attachment:
        attachment = Attachment(todo_id=todo_id, file=file)
        self.session.add(attachment)
        await self.session.commit()
        await self.session.refresh(attachment)
        return attachment
 