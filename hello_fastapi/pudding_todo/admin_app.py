from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncEngine

from .apps.account.admin import UserAdmin
from .apps.todo.admin import TodoGroupAdmin, TodoAdmin

def add_views(admin: Admin):
    admin.add_view(UserAdmin)
    admin.add_view(TodoGroupAdmin)
    admin.add_view(TodoAdmin)


def init_admin(
    app: FastAPI,
    db_engine: AsyncEngine,
    base_url: str = "/-_-/admin",
) -> Admin:
    admin = Admin(
        app,
        db_engine,
        base_url=base_url,
    )

    add_views(admin)
    return admin
