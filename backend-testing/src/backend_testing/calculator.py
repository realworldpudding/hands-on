import math

class Calculator:
    def add(self, x: float, y: float) -> float:
        """두 수를 더합니다.
        
        Examples:
            >>> calc = Calculator()
            >>> calc.add(2, 3)
            5
            >>> calc.add(-1, 1)
            0
            >>> calc.add(0.1, 0.2)  # doctest: +ELLIPSIS
            0.3...
            >>> calc.add(10.5, -3.2)
            7.3
        """
        return x + y
    
    def subtract(self, x: float, y: float) -> float:
        """첫 번째 수에서 두 번째 수를 뺍니다.
        
        Examples:
            >>> calc = Calculator()
            >>> calc.subtract(5, 3)
            2
            >>> calc.subtract(1, 1)
            0
            >>> calc.subtract(-1, -1)
            0
            >>> calc.subtract(10.5, 3.2)
            7.3
            >>> calc.subtract(0, 5)
            -5
        """
        return x - y
    
    def multiply(self, x: float, y: float) -> float:
        """두 수를 곱합니다.
        
        Examples:
            >>> calc = Calculator()
            >>> calc.multiply(2, 3)
            6
            >>> calc.multiply(-2, 3)
            -6
            >>> calc.multiply(0, 5)
            0
            >>> calc.multiply(0.5, 2)
            1.0
            >>> calc.multiply(-2, -3)
            6
        """
        return x * y
    
    def divide(self, x: float, y: float) -> float:
        """첫 번째 수를 두 번째 수로 나눕니다.
        
        Examples:
            >>> calc = Calculator()
            >>> calc.divide(6, 2)
            3.0
            >>> calc.divide(5, 2)
            2.5
            >>> calc.divide(-6, 2)
            -3.0
            >>> calc.divide(0, 5)
            0.0
            
            # 0으로 나누기 시도시 ValueError 발생
            >>> calc.divide(4, 0)
            Traceback (most recent call last):
                ...
            ValueError: 0으로 나눌 수 없습니다.
        """
        if y == 0:
            raise ValueError("0으로 나눌 수 없습니다.")
        return x / y
    
    def power(self, x: float, n: float) -> float:
        """x의 n제곱을 계산합니다.
        
        Examples:
            >>> calc = Calculator()
            >>> calc.power(2, 3)
            8.0
            >>> calc.power(2, 0)
            1.0
            >>> calc.power(2, -1)
            0.5
            >>> calc.power(4, 0.5)  # 제곱근
            2.0
            >>> calc.power(-2, 2)  # 음수의 짝수 제곱
            4.0
            >>> calc.power(-2, 3)  # 음수의 홀수 제곱
            -8.0
        """
        return math.pow(x, n)
    
    def square_root(self, x: float) -> float:
        """양수의 제곱근을 계산합니다.
        
        Examples:
            >>> calc = Calculator()
            >>> calc.square_root(4)
            2.0
            >>> calc.square_root(2)  # doctest: +ELLIPSIS
            1.4142135623730...
            >>> calc.square_root(0)
            0.0
            
            # 음수의 제곱근 시도시 ValueError 발생
            >>> calc.square_root(-1)
            Traceback (most recent call last):
                ...
            ValueError: 음수의 제곱근은 계산할 수 없습니다.
        """
        if x < 0:
            raise ValueError("음수의 제곱근은 계산할 수 없습니다.")
        return math.sqrt(x) 