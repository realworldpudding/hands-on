from sqladmin import ModelView
from starlette.requests import Request

from pudding_todo.authentication import password_helper
from .models import User


class UserAdmin(ModelView, model=User):
    column_list = (
        User.id,
        User.username,
        User.is_active,
    )
    column_searchable_list = (
        User.username,
    )
    column_sortable_list = (User.id, User.username,)
    column_default_sort = (User.id, True)
    page_size = 50

    async def on_model_change(
        self, data: dict, model: User, is_created: bool, request: Request
    ) -> None:
        if _password := data.get("hashed_password"):
            if _password != model.hashed_password:
                data["hashed_password"] = password_helper.hash(_password)
