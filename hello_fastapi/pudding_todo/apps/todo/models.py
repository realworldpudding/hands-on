from typing import Optional, TYPE_CHECKING
from datetime import datetime, UTC

from pydantic import AwareDatetime
from sqlmodel import Field, SQLModel, Text, func, Relationship
from sqlmodel.main import declared_attr
from sqlalchemy_utc import UtcDateTime

if TYPE_CHECKING:
    from pudding_todo.apps.account.models import User


class TodoGroup(SQLModel, table=True):
    id: int = Field(
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"autoincrement": True},
    )
    name: str = Field(unique=True)

    user_id: int = Field(nullable=False, foreign_key="user.id")
    user: "User" = Relationship(
        back_populates="todo_groups",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    todos: list["Todo"] = Relationship(
        back_populates="group",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    @declared_attr
    @classmethod
    def __tablename__(cls) -> str:
        return "todo_group"


class Todo(SQLModel, table=True):
    id: int = Field(
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"autoincrement": True},
    )
    name: str
    description: Optional[str] = Field(nullable=True, default=None, sa_type=Text)

    user_id: int = Field(nullable=False, foreign_key="user.id")
    user: "User" = Relationship(
        back_populates="todos",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    group_id: int = Field(nullable=False, foreign_key=f"{TodoGroup.__tablename__}.id")
    group: TodoGroup = Relationship(
        back_populates="todos",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    
    created_at: AwareDatetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )
    updated_at: AwareDatetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
            "server_onupdate": func.now(),
        },
    )
    duedate_at: Optional[AwareDatetime] = Field(
        default=None,
        nullable=True,
        sa_type=UtcDateTime,
    )
    completed_at: Optional[AwareDatetime] = Field(
        default=None,
        nullable=True,
        sa_type=UtcDateTime,
    )
    cancelled_at: Optional[AwareDatetime] = Field(
        default=None,
        nullable=True,
        sa_type=UtcDateTime,
    )
