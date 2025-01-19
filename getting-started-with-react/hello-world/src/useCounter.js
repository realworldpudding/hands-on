import { useState } from 'react';

export function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);

  const increment = () => setCount((prev) => prev + 1);
  const decrement = async () => setCount((prev) => prev - 1);

  return { count, increment, decrement };
}