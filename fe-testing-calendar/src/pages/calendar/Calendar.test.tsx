import { describe, expect, test, vi, beforeEach } from "vitest";
import { render } from "vitest-browser-react";
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { userEvent } from "@testing-library/user-event";
import { waitFor } from "@testing-library/react";

import { EnumEventKind, IEvent } from "~/types/event.d";
import { ITimeslot } from "~/types/timeslot.d";
import Calendar from "./Calendar";

const YEAR = 2024;
const MONTH = 11;

// Mock events data
const MOCK_EVENT: IEvent = {
  slug: "hannal-coffeechat",
  name: "회의",
  description: "팀 미팅",
  extra: {},
  price: {},
  participation_count: 0,
  kind: EnumEventKind.MEETUP,
  is_public: true,
  started_at: "",
  closed_at: null,
};

// Mock timeslots data
const MOCK_TIMESLOTS: ITimeslot[] = [
  {
    uid: "1",
    startTime: "09:00",
    endTime: "10:00",
    price: null
  }
];

// Mock custom hooks
vi.mock('~/hooks/useCalendarEvent', () => ({
  useCalendarEvent: () => MOCK_EVENT
}));

vi.mock('~/hooks/useCalendarNavigation', () => ({
  useCalendarNavigation: () => ({
    handlePrevious: vi.fn(),
    handleNext: vi.fn(),
  })
}));

vi.mock('~/hooks/useEventSelection', () => ({
  useEventSelection: () => ({
    handleSelectDay: vi.fn(),
  })
}));

vi.mock('~/hooks/useTimeslots', () => ({
  useTimeslots: () => ({
    data: MOCK_TIMESLOTS
  })
}));

// Mock tanstack router
vi.mock('@tanstack/react-router', async () => ({
  ...await vi.importActual('@tanstack/react-router'),
  useSearch: () => ({
    year: YEAR,
    month: MONTH,
  }),
  useParams: () => ({
    slug: MOCK_EVENT.slug,
  }),
  useNavigate: () => vi.fn(),
}));

vi.mock('@tanstack/react-query', async () => ({
  ...(await vi.importActual('@tanstack/react-query')),
  useQuery: ({ queryKey }: { queryKey: string[] }) => {
    if (queryKey[0] === 'calendarEvents') {
      return { data: [MOCK_EVENT] };
    }
    return { data: null };
  },
  useQueryClient: () => ({
    prefetchQuery: vi.fn(),
  }),
}));

describe("Calendar", () => {
  let queryClient: QueryClient;
  let container: HTMLElement;
  const baseDate = new Date(YEAR, MONTH - 1, 22);

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });

    const { container: renderedContainer } = render(
      <QueryClientProvider client={queryClient}>
        <Calendar baseDate={baseDate} />
      </QueryClientProvider>
    );
    container = renderedContainer;
  });
  
  test(`${YEAR}년 ${MONTH}월 캘린더 렌더링`, () => {
    const cells = container.querySelectorAll('tbody[role="grid"][role-label="calendar-body"] td');
    const buttonCells = container.querySelectorAll('td[role="button"][role-label^="day"]');
    
    // 11월은 30일까지 있고, 1일이 금요일이므로
    // 첫 주: 5개의 빈칸(0) + 1, 2
    // 마지막 주: 30일 + 0개의 빈칸
    // 총 7 * 5 = 35칸
    expect(cells).toHaveLength(35);
    expect(buttonCells).toHaveLength(30);
    
    // 첫 주의 금요일이 1일
    expect(cells[5].textContent).toBe('1');
    
    // 30일까지 있어야 함
    expect(cells[34].textContent).toBe('30');
  });

  test("이벤트가 있는 날짜 표시", () => {
    // 15일과 20일에 이벤트가 있음
    expect(container.querySelector('td[role="button"][role-label="day-15"]')).toBeInTheDocument();
    expect(container.querySelector('td[role="button"][role-label="day-20"]')).toBeInTheDocument();
  });

  test("Navigator 컴포넌트 렌더링", () => {
    expect(container.querySelector('[role="label"][role-label="year-month"]')).toHaveTextContent(`${YEAR}년 ${MONTH}월`);
    expect(container.querySelector('[role="button"][role-label="button-이전달"]')).toBeInTheDocument();
    expect(container.querySelector('[role="button"][role-label="button-다음달"]')).toBeInTheDocument();
  });

  test("타임슬롯 렌더링", async () => {
    // 날짜 선택
    const day_label = baseDate.getDate();
    const dayCell = container.querySelector(`td[role="button"][role-label="day-${day_label}"]`)!;
    await userEvent.click(dayCell);
    const timeslot = MOCK_TIMESLOTS[0];

    // 타임슬롯이 렌더링되었는지 확인
    expect(container.querySelector(`[role="button"][role-label="timeslot-${timeslot.uid}"]`)).toBeInTheDocument();
    expect(container.querySelector('[role="time"]')).toHaveTextContent(timeslot.startTime);
  });
});
