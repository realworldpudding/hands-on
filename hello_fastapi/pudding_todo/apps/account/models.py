from typing import Optional, TYPE_CHECKING

from starlette.authentication import BaseUser
from sqlmodel import Field, SQLModel, Relationship


if TYPE_CHECKING:
    from pudding_todo.apps.todo.models import Todo, TodoGroup

class User(BaseUser, SQLModel, table=True):
    id: int = Field(
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"autoincrement": True},
    )
    username: str = Field(unique=True)
    hashed_password: Optional[str] = Field(nullable=True, default=None, exclude=True)
    is_active: bool = Field(default=True)

    todo_groups: list["TodoGroup"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

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
