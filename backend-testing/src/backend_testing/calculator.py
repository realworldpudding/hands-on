import math

class Calculator:
    def add(self, x: float, y: float) -> float:
        """두 수를 더합니다."""
        return x + y
    
    def subtract(self, x: float, y: float) -> float:
        """첫 번째 수에서 두 번째 수를 뺍니다."""
        return x - y
    
    def multiply(self, x: float, y: float) -> float:
        """두 수를 곱합니다."""
        return x * y
    
    def divide(self, x: float, y: float) -> float:
        """첫 번째 수를 두 번째 수로 나눕니다."""
        if y == 0:
            raise ValueError("0으로 나눌 수 없습니다.")
        return x / y
    
    def power(self, x: float, n: float) -> float:
        """x의 n제곱을 계산합니다."""
        return math.pow(x, n)
    
    def square_root(self, x: float) -> float:
        """양수의 제곱근을 계산합니다."""
        if x < 0:
            raise ValueError("음수의 제곱근은 계산할 수 없습니다.")
        return math.sqrt(x)
