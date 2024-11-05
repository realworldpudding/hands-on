from uuid import UUID
from typing import Literal
from pydantic import BaseModel

from backend_testing.calculator_repository import OperationType


class CalculatePayloadSchema(BaseModel):
    session_uid: UUID
    value: int | float | OperationType | Literal["(", ")"]
