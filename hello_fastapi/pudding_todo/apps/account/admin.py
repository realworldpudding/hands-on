from sqladmin import ModelView

from .models import User


class UserAdmin(ModelView, model=User):
    category = "Account"
    name = "사용자"
    name_plural = "사용자"
    column_list = (
        User.id,
        User.username,
        User.is_active,
    )
    form_columns = (
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
    column_details_list = (
        User.id,
        User.username,
        User.is_active,
    )


