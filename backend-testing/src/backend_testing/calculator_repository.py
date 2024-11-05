from enum import Enum
from datetime import datetime, UTC
from typing import Optional, Union
import asyncio

from pydantic import BaseModel, AwareDatetime

class OperationType(Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    POWER = "power"
    SQUARE_ROOT = "square_root"
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"


class CalculationRecord(BaseModel):
    """계산 기록을 저장하는 데이터 클래스"""
    inputs: list[Union[float, OperationType, str]]
    result: float
    timestamp: AwareDatetime
    error: Optional[str] = None


class CalculatorRepository:
    def __init__(self):
        self._records: list[CalculationRecord] = []
        self._current_calculation: list[Union[float, OperationType, str]] = []
        self._lock = asyncio.Lock()

    async def add_to_current(self, value: Union[float, OperationType, str]) -> None:
        """현재 계산 중인 입력을 저장합니다."""
        async with self._lock:
            self._current_calculation.append(value)

    async def save_calculation(self, 
                             inputs: list[Union[float, OperationType, str]], 
                             result: float, 
                             error: Optional[str] = None) -> None:
        """완료된 계산을 저장합니다."""
        async with self._lock:
            record = CalculationRecord(
                inputs=inputs.copy(),
                result=result,
                timestamp=datetime.now(tz=UTC),
                error=error
            )
            self._records.append(record)

    async def get_all_records(self) -> list[CalculationRecord]:
        """모든 계산 기록을 반환합니다."""
        async with self._lock:
            return self._records.copy()

    async def clear_current(self) -> None:
        """현재 진행 중인 계산을 초기화합니다."""
        async with self._lock:
            self._current_calculation.clear()

    async def clear_all(self) -> None:
        """모든 기록을 삭제합니다."""
        async with self._lock:
            self._records.clear()
            self._current_calculation.clear()
