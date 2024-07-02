from datetime import datetime, UTC
from typing import Optional, Literal

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
@tpl.hx("partial/todo-detail.jinja2", no_data=True)
async def create_todo(
    payload: TodoCreateSchema,
    user: CurrentUserDep,
    service: TodoServiceDep,
    todo_group_service: TodoGroupServiceDep,
) -> dict:
    group = await todo_group_service.get_users_group_by_id(user.id, payload.group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    todo = await service.create(payload)
    ctx = {
        "todo": todo
    }
    return ctx


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


@router.get("/todo-groups/{pk}/todos", name="list-todo-page")
@tpl.page("pages/todo-list.jinja2")
async def list_todo(
    pk: int,
    user: CurrentUserDep,
    service: TodoServiceDep,
    todo_group_service: TodoGroupServiceDep,
    status: Optional[Literal["all", "completed", "incompleted"]] = None,
) -> dict:
    todo_group = await todo_group_service.get_users_group_by_id(user.id, pk)
    if not todo_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    
    params = {}
    match status:
        case "completed":
            params["is_completed"] = True
        case "incompleted":
            params["is_completed"] = False
        case _:
            params = {}
    
    todos = await service.findall(user.id, group_id=pk, **params)
    ctx = {
        "todo_group": todo_group,
        "todos": todos,
    }

    return ctx


@router.post("/todos/{pk}/completed", name="set-todo-completed")
@tpl.hx("partial/todo-detail.jinja2", no_data=True)
async def set_todo_to_completed(
    pk: int,
    user: CurrentUserDep,
    service: TodoServiceDep,
) -> dict:
    todo = await service.get_by_id(pk)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    now = datetime.now(UTC)    
    todo = await service.set_completed_at(user.id, todo, now)
    ctx = {
        "todo": todo,
    }
    return ctx


@router.delete("/todos/{pk}/completed", name="unset-todo-completed")
@tpl.hx("partial/todo-detail.jinja2", no_data=True)
async def unset_todo_to_completed(
    pk: int,
    user: CurrentUserDep,
    service: TodoServiceDep,
) -> dict:
    todo = await service.get_by_id(pk)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    
    todo = await service.set_completed_at(user.id, todo)
    ctx = {
        "todo": todo,
    }
    return ctx
