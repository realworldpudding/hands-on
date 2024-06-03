from typing import Optional
from pydantic import BaseModel, Field


class TodoCreateSchema(BaseModel):
    name: str
    description: Optional[str] = Field(default=None)
