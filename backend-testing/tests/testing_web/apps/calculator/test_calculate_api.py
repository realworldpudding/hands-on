import pytest
from uuid import uuid4
from httpx import AsyncClient
from backend_testing.calculator_service import CalculatorService
from backend_testing.calculator_repository import OperationType

@pytest.fixture
def calculator_service():
    return CalculatorService()

@pytest.fixture
def session_uid():
    return uuid4()


async def test_calculate_endpoint_success(client: AsyncClient, calculator_service, session_uid):
    # 테스트 데이터 준비
    payload = {
        "session_uid": str(session_uid),
        "value": 5.0
    }

    # API 호출
    response = await client.post("/calculator/calculate", json=payload)
    
    # 응답 검증
    print()
    print(response.json())
    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)
    assert len(history) > 0
    
    # 마지막 기록 검증
    last_record = history[-1]
    assert isinstance(last_record, float)
    assert last_record == 5.0


async def test_calculate_endpoint_invalid_session(client: AsyncClient, session_uid):
    # 잘못된 세션 ID로 테스트
    payload = {
        "session_uid": "invalid-uuid",
        "value": 5.0
    }
    
    response = await client.post("/calculator/calculate", json=payload)
    assert response.status_code == 422  # 유효성 검증 실패


async def test_calculate_endpoint_invalid_value(client: AsyncClient, session_uid):
    # 잘못된 입력값으로 테스트
    payload = {
        "session_uid": str(session_uid),
        "value": "invalid"  # 숫자나 연산자가 아닌 값
    }
    
    response = await client.post("/calculator/calculate", json=payload)
    assert response.status_code == 422


async def test_calculate_endpoint_complex_expression(client: AsyncClient, session_uid):
    # 복잡한 수식 테스트
    expressions = [
        {"session_uid": str(session_uid), "value": 2.0},
        {"session_uid": str(session_uid), "value": OperationType.ADD.value},
        {"session_uid": str(session_uid), "value": 3.0},
        {"session_uid": str(session_uid), "value": OperationType.MULTIPLY.value},
        {"session_uid": str(session_uid), "value": 4.0}
    ]
    
    last_response = None
    for expr in expressions:
        last_response = await client.post("/calculator/calculate", json=expr)
        assert last_response.status_code == 200
    
    # 최종 히스토리 검증
    history = last_response.json()
    assert isinstance(history, list)
    last_record = history[-1]
    assert isinstance(last_record, float)
    assert last_record == 4.0


async def test_calculate_endpoint_with_parentheses(client: AsyncClient, session_uid):
    # 괄호가 포함된 수식 테스트
    expressions = [
        {"session_uid": str(session_uid), "value": "("},
        {"session_uid": str(session_uid), "value": 2.0},
        {"session_uid": str(session_uid), "value": OperationType.ADD.value},
        {"session_uid": str(session_uid), "value": 3.0},
        {"session_uid": str(session_uid), "value": ")"},
        {"session_uid": str(session_uid), "value": OperationType.MULTIPLY.value},
        {"session_uid": str(session_uid), "value": 4.0}
    ]
    
    last_response = None
    for expr in expressions:
        last_response = await client.post("/calculator/calculate", json=expr)
        assert last_response.status_code == 200
    
    history = last_response.json()
    assert isinstance(history, list)
    assert len(history) > 0
