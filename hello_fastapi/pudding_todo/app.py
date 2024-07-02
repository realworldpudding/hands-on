from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from pudding_todo.apps.account.router import router as account_router
from pudding_todo.apps.common.router import router as common_router
from pudding_todo.apps.todo.router import router as todo_router

from .admin_app import init_admin
from .authentication import fastapi_users, auth_backend
from .db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(common_router)
    app.include_router(account_router)
    app.include_router(todo_router)
    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )

    app.mount(
        "/_uploads",
        StaticFiles(directory="_uploads"),
        name="uploads",
    )
    return app

app = create_app()

init_admin(app, engine)
