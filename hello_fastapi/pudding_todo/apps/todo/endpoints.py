from fastapi import APIRouter, status, HTTPException

from pudding_todo.authentication import CurrentUserDep

from .deps import TodoGroupServiceDep, TodoServiceDep
from .models import Todo
from .schemas import TodoCreateSchema

router = APIRouter(prefix="/todos")


@router.post(
    "/",
    response_model=Todo,
    name="create-todo",
    status_code=status.HTTP_201_CREATED,
)
async def create_todo(
    payload: TodoCreateSchema,
    user: CurrentUserDep,
    service: TodoServiceDep,
    todo_group_service: TodoGroupServiceDep,
) -> Todo:
    group = await todo_group_service.get_users_group_by_id(user.id, payload.group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    todo = await service.create(payload)
    return todo
