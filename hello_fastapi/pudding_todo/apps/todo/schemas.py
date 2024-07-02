from typing import Optional, Annotated
from pydantic import BaseModel, Field, AwareDatetime, BeforeValidator

class TodoGroupCreateSchema(BaseModel):
    name: str


BlankableAwareDatetime = Annotated[
    AwareDatetime | None,
    BeforeValidator(lambda v: None if v == "" else v),
]

class TodoCreateSchema(BaseModel):
    name: str
    description: Optional[str] = Field(default=None)
    duedate_at: BlankableAwareDatetime = Field(default=None)
    group_id: int
