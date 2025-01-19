import { describe, test, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react-hooks'; 
import { useCounter } from './useCounter';

describe('useCounter 커스텀 훅 테스트', () => {
  test('초기값을 잘 설정해야 한다.', () => {
    const { result } = renderHook(() => useCounter(5));
    expect(result.current.count).toBe(5);
  });

  test('increment 함수를 호출하면 count가 1 증가한다.', () => {
    const { result } = renderHook(() => useCounter());
    
    act(() => {
      result.current.increment();
    });
    
    expect(result.current.count).toBe(1);
  });

  test('decrement 함수를 호출하면 count가 1 감소한다.', async () => {
    const { result } = renderHook(() => useCounter(2));

    await act(async () => {
      await result.current.decrement();
    });

    expect(result.current.count).toBe(1);
  });
});