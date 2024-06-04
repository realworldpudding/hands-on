from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_users import BaseUserManager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel

from pudding_todo.app import create_app
from pudding_todo.authentication import use_user_db, use_user_manager
from pudding_todo.db import use_session
from pudding_todo.apps.account.models import User


@pytest.fixture()
async def db_session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///file:testing.db?mode=memory&cache=shared&uri=true",
        future=True,
        echo=False,
        poolclass=NullPool,
    )

    async with engine.connect() as conn:
        await conn.begin()
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
   
        session_class = async_sessionmaker(
            conn, class_=AsyncSession, expire_on_commit=False, autoflush=False,
        )
        async with session_class() as session:
            yield session
            
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.rollback()

    await engine.dispose()


@pytest.fixture(autouse=True)
def fastapi_app(db_session: AsyncSession) -> Generator[FastAPI, None, None]:
    app = create_app()
    app.dependency_overrides[use_session] = lambda: db_session
    yield app


@pytest.fixture()
def client(fastapi_app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(fastapi_app) as test_client:
        yield test_client


@pytest.fixture()
async def user_manager(db_session):
    user_db = await anext(use_user_db(db_session))
    yield await anext(use_user_manager(user_db))


@pytest.fixture()
async def valid_user(db_session, user_manager: BaseUserManager):
    password = "PuddingCamp2024"
    hashed_password = user_manager.password_helper.hash(password)

    user = User(username="puddingcamp", hashed_password=hashed_password)
    db_session.add(user)
    await db_session.commit()
    yield user


@pytest.fixture()
async def valid_user2(db_session, user_manager: BaseUserManager):
    password = "PuddingCamp2024"
    hashed_password = user_manager.password_helper.hash(password)

    user = User(username="puddingcamp2", hashed_password=hashed_password)
    db_session.add(user)
    await db_session.commit()
    yield user
