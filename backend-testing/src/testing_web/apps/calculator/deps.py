from uuid import UUID
from typing import Annotated
from fastapi import Depends, Header, HTTPException, status

from backend_testing.calculator_service import CalculatorService


def current_user_session_uid(authorization: UUID | None = Header(default=None)) -> UUID:
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return authorization


CurrentUserSessionUIDDep = Annotated[UUID, Depends(current_user_session_uid)]


def get_calculator_service() -> CalculatorService:
    return CalculatorService()


CalculatorServiceDep = Annotated[CalculatorService, Depends(get_calculator_service)]
