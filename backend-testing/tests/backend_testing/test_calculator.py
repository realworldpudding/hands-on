import pytest
from backend_testing.calculator import Calculator

class TestCalculator:
    @pytest.fixture
    def calculator(self):
        return Calculator()
    
    def test_add(self, calculator):
        assert calculator.add(2, 3) == 5
        assert calculator.add(-1, 1) == 0
        assert calculator.add(0.1, 0.2) == pytest.approx(0.3)
    
    def test_subtract(self, calculator):
        assert calculator.subtract(5, 3) == 2
        assert calculator.subtract(1, 1) == 0
        assert calculator.subtract(-1, -1) == 0
    
    def test_multiply(self, calculator):
        assert calculator.multiply(2, 3) == 6
        assert calculator.multiply(-2, 3) == -6
        assert calculator.multiply(0, 5) == 0
    
    def test_divide(self, calculator):
        assert calculator.divide(6, 2) == 3
        assert calculator.divide(5, 2) == 2.5
        assert calculator.divide(-6, 2) == -3
        
        with pytest.raises(ValueError, match="0으로 나눌 수 없습니다."):
            calculator.divide(4, 0)
    
    def test_power(self, calculator):
        assert calculator.power(2, 3) == 8
        assert calculator.power(2, 0) == 1
        assert calculator.power(2, -1) == 0.5
    
    def test_square_root(self, calculator):
        assert calculator.square_root(4) == 2
        assert calculator.square_root(2) == pytest.approx(1.4142135623730951)
        assert calculator.square_root(0) == 0
        
        with pytest.raises(ValueError, match="음수의 제곱근은 계산할 수 없습니다."):
            calculator.square_root(-1) 