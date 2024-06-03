from fastapi import APIRouter, status

from pudding_todo.authentication import CurrentUserDep

from .deps import TodoServiceDep
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
) -> Todo:
    todo = await service.create(user.id, payload)
    return todo
