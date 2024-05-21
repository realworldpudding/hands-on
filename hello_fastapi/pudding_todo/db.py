from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

engine = create_async_engine(
    "sqlite+aiosqlite:///./pudding_todo.db",
    future=True,
    echo=True,
    poolclass=NullPool,
)


async def use_session():
    session_class = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, autoflush=False,
    )
    async with session_class() as session:
        yield session


DbSessionDep = Annotated[AsyncSession, Depends(use_session)]
