from contextlib import asynccontextmanager

from fastapi import FastAPI

from pudding_todo.apps.account.router import router as account_router
from pudding_todo.apps.common.router import router as common_router

from .db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(common_router)
    app.include_router(account_router)
    return app

app = create_app()
