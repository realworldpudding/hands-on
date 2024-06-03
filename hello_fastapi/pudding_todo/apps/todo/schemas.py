from typing import Optional
from pydantic import BaseModel, Field


class TodoGroupCreateSchema(BaseModel):
    name: str


class TodoCreateSchema(BaseModel):
    name: str
    description: Optional[str] = Field(default=None)
    group_id: int
