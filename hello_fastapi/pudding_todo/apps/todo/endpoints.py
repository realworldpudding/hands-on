from fastapi import APIRouter, status, HTTPException

from pudding_todo.authentication import CurrentUserDep
from pudding_todo.templates import tpl

from .deps import TodoGroupServiceDep, TodoServiceDep
from .models import Todo
from .schemas import TodoCreateSchema

router = APIRouter()


@router.post(
    "/todos",
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


@router.get("/todo-groups", name="list-todo-group-page")
@tpl.page("pages/todo-group-list.jinja2")
async def list_todo_group(
    user: CurrentUserDep,
    service: TodoGroupServiceDep,
) -> dict:
    groups = await service.findall(user.id)
    ctx = {
        "groups": groups,
        "user": user,
    }

    return ctx


@router.get("/~/todo-group-todo-count/{pk}", name="partial-todo-group-todos-count")
@tpl.hx("partial/todo-group-todos-count.jinja2", no_data=True)
async def count_todo_group_todos(
    pk: int,
    user: CurrentUserDep,
    service: TodoServiceDep,
) -> dict:
    count = await service.count_by_group_id(user.id, pk)
    ctx = {
        "count_all": count,
    }
    return ctx
