import { useCounter } from './useCounter';

export function Counter() {
  const { count, increment, decrement } = useCounter(0);

  return (
    <div>
      <p>현재 카운트: {count}</p>
      
      <button
        type="button"
        role="button"
        aria-label="감소"
        onClick={decrement}>
            감소
        </button>
      <button
        type="button"
        role="button"
        aria-label="증가"
        onClick={increment}>
            증가
        </button>
    </div>
  );
}