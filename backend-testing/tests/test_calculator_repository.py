from uuid import uuid4, UUID
import asyncio
import pytest
from datetime import datetime
from backend_testing.calculator_repository import (
    CalculatorRepository,
    OperationType,
)


@pytest.fixture
async def repository():
    repo = CalculatorRepository()
    yield repo
    await repo.clear_all()


async def test_add_to_current(repository: CalculatorRepository):
    """현재 계산에 값 추가 테스트"""
    await repository.add_to_current(2)
    await repository.add_to_current(OperationType.ADD)
    await repository.add_to_current(3)
    
    async with repository._lock:
        assert len(repository._current_calculation) == 3
        assert repository._current_calculation[0] == 2
        assert repository._current_calculation[1] == OperationType.ADD
        assert repository._current_calculation[2] == 3


async def test_save_calculation(repository: CalculatorRepository):
    """계산 결과 저장 테스트"""
    inputs = [2, OperationType.ADD, 3]
    result = 5
    
    await repository.save_calculation(inputs, result)
    
    records = await repository.get_all_records()
    assert len(records) == 1
    assert records[0].inputs == inputs
    assert records[0].result == result
    assert isinstance(records[0].timestamp, datetime)
    assert records[0].error is None


async def test_save_calculation_with_error(repository: CalculatorRepository):
    """에러가 있는 계산 결과 저장 테스트"""
    inputs = [5, OperationType.DIVIDE, 0]
    result = 0
    error = "0으로 나눌 수 없습니다."
    
    await repository.save_calculation(inputs, result, error)
    
    records = await repository.get_all_records()
    assert len(records) == 1
    assert records[0].error == error


@pytest.mark.asyncio
async def test_clear_current(repository: CalculatorRepository):
    """현재 계산 초기화 테스트"""
    await repository.add_to_current(2)
    await repository.add_to_current(OperationType.ADD)
    await repository.add_to_current(3)
    
    await repository.clear_current()
    
    async with repository._lock:
        assert len(repository._current_calculation) == 0


@pytest.mark.asyncio
async def test_clear_all(repository: CalculatorRepository):
    """모든 기록 초기화 테스트"""
    # 현재 계산에 값 추가
    await repository.add_to_current(2)
    await repository.add_to_current(OperationType.ADD)
    
    # 완료된 계산 저장
    await repository.save_calculation([2, OperationType.ADD, 3], 5)
    await repository.save_calculation([4, OperationType.MULTIPLY, 2], 8)
    
    await repository.clear_all()
    
    async with repository._lock:
        assert len(repository._current_calculation) == 0
        assert len(repository._records) == 0


async def test_concurrent_access(repository: CalculatorRepository):
    """동시성 테스트"""
    async def add_and_save():
        await repository.add_to_current(1)
        await repository.add_to_current(OperationType.ADD)
        await repository.add_to_current(2)
        await repository.save_calculation([1, OperationType.ADD, 2], 3)
    
    # 여러 작업을 동시에 실행
    tasks = [add_and_save() for _ in range(5)]
    await asyncio.gather(*tasks)
    
    records = await repository.get_all_records()
    assert len(records) == 5
