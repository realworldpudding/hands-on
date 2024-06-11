from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncEngine

from .apps.account.admin import UserAdmin

def add_views(admin: Admin):
    admin.add_view(UserAdmin)


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
