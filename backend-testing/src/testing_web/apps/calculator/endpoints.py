from fastapi import APIRouter, HTTPException, Request

from .deps import CalculatorServiceDep
from .schemas import CalculatePayloadSchema

router = APIRouter()


@router.post("/calculate")
async def calculate(payload: CalculatePayloadSchema, calculator_service: CalculatorServiceDep):
    calculator_service.set_session_uid(payload.session_uid)
    try:
        await calculator_service.add_input(payload.value)
        return await calculator_service.get_current_calculation()
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
