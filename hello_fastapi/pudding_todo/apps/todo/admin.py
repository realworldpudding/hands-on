from typing import ClassVar

from sqladmin import ModelView

from .models import TodoGroup, Todo


class TodoGroupAdmin(ModelView, model=TodoGroup):
    category = "Todo"
    name = "할 일 그룹"
    name_plural = "할 일 그룹"
    column_list = (
        TodoGroup.id,
        TodoGroup.name,
        TodoGroup.user,
    )
    form_columns = (
        TodoGroup.name,
        TodoGroup.user,
    )
    column_searchable_list = (
        TodoGroup.id,
        TodoGroup.name,
    )
    column_sortable_list = (TodoGroup.id, TodoGroup.name, TodoGroup.user,)
    column_default_sort = (TodoGroup.id, True)

    form_ajax_refs: ClassVar = {
        "user": {
            "fields": ("id", "username"),
            "order_by": "id",
        },
    }


class TodoAdmin(ModelView, model=Todo):
    category = "Todo"
    name = "할 일"
    name_plural = "할 일들"
    column_list = (
        Todo.id,
        Todo.name,
        Todo.group,
        Todo.created_at,
        Todo.updated_at,
        Todo.duedate_at,
        Todo.completed_at,
        Todo.cancelled_at,
    )
    form_columns = (
        Todo.name,
        Todo.group,
        Todo.description,
        Todo.duedate_at,
        Todo.completed_at,
        Todo.cancelled_at,
    )
    column_searchable_list = (
        Todo.id,
        Todo.name,
    )
    column_sortable_list = (Todo.id, Todo.name, Todo.group,)
    column_default_sort = (Todo.id, True)

    form_ajax_refs: ClassVar = {
        "group": {
            "fields": ("id", "name"),
            "order_by": "id",
        },
    }
