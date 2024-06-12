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
