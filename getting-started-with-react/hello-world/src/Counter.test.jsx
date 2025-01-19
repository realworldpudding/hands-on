import { describe, test, expect } from 'vitest';
import { render } from '@testing-library/react';
import userEvent from "@testing-library/user-event";

import { Counter } from './Counter';

describe('Counter 컴포넌트 테스트', () => {
  test('버튼을 클릭하면 카운트가 증가한다.', async () => {
    const user = userEvent.setup();
 
    const { getByLabelText, getByText } = render(<Counter />);
    const button = getByLabelText('증가');
    const countText = getByText(/현재 카운트: 0/);

    // 초기 상태 확인
    expect(countText).toBeInTheDocument();

    // 버튼 클릭 이벤트 시뮬레이션
    await user.click(button);

    // 다시 렌더링된 상태 확인
    expect(getByText(/현재 카운트: 1/)).toBeInTheDocument();
  });
});
