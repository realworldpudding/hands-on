from uuid import UUID
from typing import List, Union
from collections import defaultdict
from .calculator_repository import CalculatorRepository, CalculationRecord, OperationType



class CalculatorService:
    _repositories: dict[UUID, CalculatorRepository]
    _current_calculation: dict[UUID, list[Union[float, OperationType, str]]]

    def __init__(self):
        self._current_session_uid: UUID | None = None
        self._repositories = defaultdict(CalculatorRepository)
        self._current_calculation = defaultdict(list)

    def set_session_uid(self, session_uid: UUID) -> None:
        self._current_session_uid = session_uid

    async def add_input(self, value: Union[float, OperationType, str]) -> None:
        """계산기에 새로운 입력을 추가합니다."""

        if self._current_session_uid is None:
            raise ValueError("세션 ID가 설정되지 않았습니다.")

        if isinstance(value, str):
            if value not in ["(", ")"]:
                raise ValueError(f"인식할 수 없는 입력값입니다: {value}")
        self._current_calculation[self._current_session_uid].append(value)
        await self._repositories[self._current_session_uid].add_to_current(value)

    async def calculate(self) -> float:
        """현재까지의 입력을 계산하고 결과를 반환합니다."""

        if self._current_session_uid is None:
            raise ValueError("세션 ID가 설정되지 않았습니다.")
        
        if not self._current_calculation:
            return 0.0

        result = await self._process_calculation()
        await self._repositories[self._current_session_uid].save_calculation(self._current_calculation[self._current_session_uid], result)
        self._current_calculation[self._current_session_uid].clear()
        return result

    async def _process_calculation(self) -> float:
        """입력된 수식을 계산합니다."""

        if self._current_session_uid is None:
            raise ValueError("세션 ID가 설정되지 않았습니다.")

        tokens = self._current_calculation[self._current_session_uid]
        if not tokens or (not isinstance(tokens[0], (int, float)) and tokens[0] not in [OperationType.LEFT_PAREN, OperationType.LEFT_PAREN.value]):
            raise ValueError(f"첫 번째 입력값은 숫자 또는 여는 괄호여야 합니다: tl {tokens[0]}")

        # 연산자 우선순위 정의
        precedence = {
            OperationType.POWER: 3,
            OperationType.MULTIPLY: 2,
            OperationType.DIVIDE: 2,
            OperationType.ADD: 1,
            OperationType.SUBTRACT: 1,
            OperationType.LEFT_PAREN: 0,
        }

        def infix_to_postfix(tokens):
            output = []
            operators = []
            
            for token in tokens:
                if isinstance(token, (int, float)):
                    output.append(float(token))
                elif token == "(" or token == OperationType.LEFT_PAREN:
                    operators.append(OperationType.LEFT_PAREN)
                elif token == ")" or token == OperationType.RIGHT_PAREN:
                    while operators and operators[-1] != OperationType.LEFT_PAREN:
                        output.append(operators.pop())
                    if operators and operators[-1] == OperationType.LEFT_PAREN:
                        operators.pop()
                    else:
                        raise ValueError("괄호가 맞지 않습니다.")
                elif isinstance(token, OperationType):
                    while (operators and 
                           operators[-1] != OperationType.LEFT_PAREN and
                           precedence[operators[-1]] >= precedence[token]):
                        output.append(operators.pop())
                    operators.append(token)
            
            while operators:
                if operators[-1] == OperationType.LEFT_PAREN:
                    raise ValueError("괄호가 맞지 않습니다.")
                output.append(operators.pop())
                
            return output

        def evaluate_postfix(tokens):
            stack = []
            
            for token in tokens:
                if isinstance(token, (int, float)):
                    stack.append(float(token))
                else:
                    if len(stack) < 2:
                        raise ValueError("잘못된 수식 형식입니다.")
                    
                    b = stack.pop()
                    a = stack.pop()
                    
                    if token == OperationType.ADD:
                        stack.append(a + b)
                    elif token == OperationType.SUBTRACT:
                        stack.append(a - b)
                    elif token == OperationType.MULTIPLY:
                        stack.append(a * b)
                    elif token == OperationType.DIVIDE:
                        if b == 0:
                            raise ValueError("0으로 나눌 수 없습니다.")
                        stack.append(a / b)
                    elif token == OperationType.POWER:
                        stack.append(pow(a, b))
            
            if len(stack) != 1:
                raise ValueError("잘못된 수식 형식입니다.")
            
            return stack[0]

        postfix = infix_to_postfix(tokens)
        return evaluate_postfix(postfix)

    async def clear(self) -> None:
        """현재 계산을 초기화합니다."""

        if self._current_session_uid is None:
            raise ValueError("세션 ID가 설정되지 않았습니다.")

        self._current_calculation[self._current_session_uid].clear()
        await self._repositories[self._current_session_uid].clear_current()

    async def get_history(self) -> list[CalculationRecord]:
        """계산 히스토리를 반환합니다."""

        if self._current_session_uid is None:
            raise ValueError("세션 ID가 설정되지 않았습니다.")
        
        return await self._repositories[self._current_session_uid].get_all_records()

    async def get_current_calculation(self) -> list[Union[float, OperationType, str]]:
        """현재 계산 상태를 반환합니다."""

        if self._current_session_uid is None:
            raise ValueError("세션 ID가 설정되지 않았습니다.")

        return await self._repositories[self._current_session_uid].get_all_current_calculation()
