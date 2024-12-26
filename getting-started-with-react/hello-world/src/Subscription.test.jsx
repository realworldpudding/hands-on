import { describe, expect, vi, beforeEach, test } from 'vitest';
import { render } from '@testing-library/react';
import Subscription from './Subscription';
import userEvent from "@testing-library/user-event";

describe('Subscription 컴포넌트', () => {
  beforeEach(() => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
  });

  test('초기 렌더링이 예상대로 이루어지는지 스냅샷으로확인한다.', () => {
    const mockOnSubscribe = vi.fn();
    const { container } = render(
      <Subscription buttonLabel="구독하기" onSubscribe={mockOnSubscribe}>
        뉴스레터 구독 안내
      </Subscription>
    );

    // 스냅샷 테스트: container의 DOM 구조를 기록하여 비교
    expect(container).toMatchSnapshot();
  });

  test('기본 Props를 전달하면 예상한 렌더링 결과를 반환한다.', () => {
    const onSubscribe = vi.fn();
    const { container } = render(
      <Subscription buttonLabel="구독하기" onSubscribe={onSubscribe}>
        <h2>구독 폼</h2>
      </Subscription>
    );

    expect(container.querySelector('h2').textContent).toBe('구독 폼');
    expect(container.querySelector('input').placeholder).toBe('이메일 주소를 입력해주세요');
    expect(container.querySelector('button').textContent).toBe('구독하기');
  });

  test('이메일 입력 변경을 처리한다.', async () => {
    const user = userEvent.setup();
    const onSubscribe = vi.fn();
    const { getByPlaceholderText } = render(
      <Subscription buttonLabel="구독하기" onSubscribe={onSubscribe}>
        구독 폼
      </Subscription>
    );

    const input = getByPlaceholderText('이메일 주소를 입력해주세요');
    await user.type(input, 'test@example.com');
    
    expect(input.value).toBe('test@example.com');
  });

  test('구독 버튼을 클릭하면 이메일을 전달한다.', async () => {
    const user = userEvent.setup();
    const onSubscribe = vi.fn();
    const { getByPlaceholderText, getByRole } = render(
      <Subscription buttonLabel="구독하기" onSubscribe={onSubscribe}>
        구독 폼
      </Subscription>
    );

    const input = getByPlaceholderText('이메일 주소를 입력해주세요');

    await user.type(input, 'test@example.com');
    await user.click(getByRole('button', { name: '구독하기' }));

    expect(onSubscribe).toHaveBeenCalledWith('test@example.com');
  });

  test('함수를 전달하면 예상한 렌더링 결과를 반환한다.', () => {
    const onSubscribe = vi.fn();
    const { container } = render(
      <Subscription buttonLabel="구독하기" onSubscribe={onSubscribe}>
        {(title, email) => (
          <div>
            <h2>{title}</h2>
            <p role="paragraph" role-label="현재 이메일">현재 이메일: {email}</p>
          </div>
        )}
      </Subscription>
    );

    expect(container.querySelector('h2').textContent).toBe('학습과 성장 컨텐츠 소식');
    expect(container.querySelector('p[role="paragraph"][role-label="현재 이메일"]').textContent).toBe('현재 이메일: ');
  });

  test('이메일이 비어있으면 자동으로 입력 창에 포커스를 준다.', () => {
    const onSubscribe = vi.fn();
    const { container } = render(
      <Subscription buttonLabel="구독하기" onSubscribe={onSubscribe}>
        구독 폼
      </Subscription>
    );

    const input = container.querySelector('input[placeholder="이메일 주소를 입력해주세요"]');
    expect(document.activeElement).not.toBe(input);
    
    // 5초 후에 포커스가 적용되는지 확인
    vi.advanceTimersByTime(5000);

    expect(document.activeElement).toBe(input);
  });

  test('이메일이 비어있지 않으면 자동으로 입력 창에 포커스가 적용되지 않는다.', async () => {
    const user = userEvent.setup();
    const onSubscribe = vi.fn();
    const { container } = render(
      <Subscription buttonLabel="구독하기" onSubscribe={onSubscribe}>
        <input type="text" placeholder="이름을 입력해주세요" />
      </Subscription>
    );

    const input = container.querySelector('input[placeholder="이메일 주소를 입력해주세요"]');
    const nameInput = container.querySelector('input[placeholder="이름을 입력해주세요"]');

    // 5초 후에 포커스가 적용되는지 확인
    vi.advanceTimersByTime(5100);
    expect(document.activeElement).toBe(input);
    await user.type(input, 'test@example.com');
    
    // 현재 활성 요소를 다른 곳으로 변경
    await user.type(nameInput, 'PuddingCamp');
    expect(document.activeElement).toBe(nameInput);
    expect(document.activeElement).not.toBe(input);

    // 5초 후에 포커스가 적용이 안 되는지 확인
    vi.advanceTimersByTime(5100);

    // 포커스가 적용되는지 확인
    expect(document.activeElement).toBe(nameInput);
    expect(document.activeElement).not.toBe(input);
  });
}); 