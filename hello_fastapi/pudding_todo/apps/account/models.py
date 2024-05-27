from typing import Optional

from starlette.authentication import BaseUser
from sqlmodel import Field, SQLModel


class User(BaseUser, SQLModel, table=True):
    id: int = Field(
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"autoincrement": True},
    )
    username: str = Field(unique=True)
    hashed_password: Optional[str] = Field(nullable=True, default=None, exclude=True)

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username

    @property
    def identity(self) -> str:
        return self.username

    @property
    def password(self) -> str:
        return self.hashed_password