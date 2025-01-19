/* global global */

import { describe, test, expect, beforeEach, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { UserProfile } from './UserProfile';

import { render } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

function renderWithQueryClient(ui) {
  return render(
    <QueryClientProvider client={queryClient}>
      {ui}
    </QueryClientProvider>
  );
}
describe('UserProfile', () => {
  beforeEach(() => {
    // 각 테스트마다 fetch를 mock
    global.fetch = vi.fn();
  });

  test('로딩 중 상태를 표시해야 한다', async () => {
    // fetch 호출 시 아직 응답이 도착하지 않은 상황을 가정
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => new Promise(() => {}), // 영원히 대기하는 Promise
    });

    renderWithQueryClient(<UserProfile userId={1} />);

    // 렌더링 직후, 로딩 메시지가 보여야 함
    expect(screen.getByText(/Loading user data.../i)).toBeInTheDocument();
  });

  test('정상적으로 사용자 데이터를 가져오면 이름과 이메일을 표시한다', async () => {
    // Mock 데이터 준비
    const mockUser = { id: 1, name: 'Alice', email: 'alice@example.com' };

    // 정상 응답
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockUser,
    });

    renderWithQueryClient(<UserProfile userId={1} />);

    // 비동기 데이터 렌더링을 기다리기 위해 waitFor 사용
    await waitFor(() => {
      expect(screen.getByText('Alice')).toBeInTheDocument();
      expect(screen.getByText('alice@example.com')).toBeInTheDocument();
    });
  });

  test('API 호출이 실패하면 에러 메시지를 표시한다', async () => {
    // 에러 응답
    global.fetch.mockResolvedValueOnce({
      ok: false,
    });

    renderWithQueryClient(<UserProfile userId={999} />);

    await waitFor(() => {
      expect(screen.getByText(/Error loading user data/i)).toBeInTheDocument();
    });
  });
});