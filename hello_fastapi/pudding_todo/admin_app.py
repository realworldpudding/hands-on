from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncEngine


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
    return admin
