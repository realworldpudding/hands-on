import pytest
from src.backend_testing.calculator_service import CalculatorService
from src.backend_testing.calculator_repository import (
    CalculatorRepository,
    OperationType
)


@pytest.fixture
async def calculator():
    repository = CalculatorRepository()
    calculator = CalculatorService(repository)
    yield calculator
    await calculator.clear()


@pytest.mark.parametrize(
    "inputs, expected",
    [
        # (입력값들, 예상 결과)
        ([2, OperationType.ADD, 3], 5),
        ([5, OperationType.SUBTRACT, 2], 3),
        ([4, OperationType.MULTIPLY, 3], 12),
        ([8, OperationType.DIVIDE, 2], 4),
        ([2, OperationType.POWER, 3], 8)
    ]
)
async def test_basic_operations(calculator: CalculatorRepository, inputs, expected):
    """기본 연산 테스트"""

    await calculator.clear()
    for value in inputs:
        await calculator.add_input(value)
    result = await calculator.calculate()
    assert result == expected


async def test_operator_precedence(calculator: CalculatorRepository):
    """연산자 우선순위 테스트"""
    # 2 + 3 * 4 = 14 (곱셈 먼저)
    inputs = [2, OperationType.ADD, 3, OperationType.MULTIPLY, 4]
    for value in inputs:
        await calculator.add_input(value)
    result = await calculator.calculate()
    assert result == 14


async def test_parentheses(calculator: CalculatorRepository):
    """괄호 연산 테스트"""
    # (2 + 3) * 4 = 20
    inputs = [
        "(", 2, OperationType.ADD, 3, ")", 
        OperationType.MULTIPLY, 4
    ]
    for value in inputs:
        await calculator.add_input(value)
    result = await calculator.calculate()
    assert result == 20


async def test_complex_calculation(calculator: CalculatorRepository):
    """복잡한 수식 테스트"""
    # (2 + 3) * 4 - 5 ^ 2 = -5
    inputs = [
        "(", 2, OperationType.ADD, 3, ")", 
        OperationType.MULTIPLY, 4,
        OperationType.SUBTRACT, 
        5, OperationType.POWER, 2
    ]
    for value in inputs:
        await calculator.add_input(value)
    result = await calculator.calculate()
    assert result == -5


async def test_error_handling(calculator: CalculatorRepository):
    """에러 처리 테스트"""
    # 0으로 나누기
    await calculator.add_input(5)
    await calculator.add_input(OperationType.DIVIDE)
    await calculator.add_input(0)
    
    with pytest.raises(ValueError, match="0으로 나눌 수 없습니다."):
        await calculator.calculate()


async def test_invalid_input(calculator: CalculatorRepository):
    """잘못된 입력 테스트"""
    # 잘못된 문자열 입력
    with pytest.raises(ValueError, match="인식할 수 없는 입력값입니다:"):
        await calculator.add_input("x")


async def test_calculation_history(calculator: CalculatorRepository):
    """계산 히스토리 테스트"""
    # 첫 번째 계산: 2 + 3 = 5
    await calculator.add_input(2)
    await calculator.add_input(OperationType.ADD)
    await calculator.add_input(3)
    result1 = await calculator.calculate()
    assert result1 == 5
    
    # 두 번째 계산: 4 * 2 = 8
    await calculator.add_input(4)
    await calculator.add_input(OperationType.MULTIPLY)
    await calculator.add_input(2)
    result2 = await calculator.calculate()
    assert result2 == 8
    
    # 히스토리 확인
    history = await calculator.get_history()
    assert len(history) == 2
    assert history[0].result == 5
    assert history[1].result == 8


async def test_clear(calculator: CalculatorRepository):
    """초기화 테스트"""
    await calculator.add_input(2)
    await calculator.add_input(OperationType.ADD)
    await calculator.add_input(3)
    
    await calculator.clear()
    
    # 현재 계산이 비어있는지 확인
    assert len(calculator._current_calculation) == 0
    
    # 새로운 계산이 가능한지 확인
    await calculator.add_input(4)
    await calculator.add_input(OperationType.MULTIPLY)
    await calculator.add_input(2)
    result = await calculator.calculate()
    assert result == 8
