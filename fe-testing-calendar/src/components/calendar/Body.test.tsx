import { describe, expect, test, vi } from "vitest";
import { render } from "vitest-browser-react";
import userEvent from "@testing-library/user-event";

import Body from "~/components/calendar/Body";

describe("Calendar Body", () => {
  test("renders empty cells for zeros and numbers for non-zero values", () => {
    const year = 2024;
    const month = 11;
    const days = [0, 0, 1, 2, 3, 4, 5];
    const onSelectDay = vi.fn();

    const { container } = render(
      <Body year={year} month={month} days={days} onSelectDay={onSelectDay} />
    );
    
    const cells = container.querySelectorAll('td');
    expect(cells).toHaveLength(7);
    
    // 첫 두 셀은 비어있어야 함
    expect(cells[0].textContent).toBe('');
    expect(cells[1].textContent).toBe('');
    
    // 나머지 셀들은 1부터 5까지의 숫자를 포함해야 함
    expect(cells[2].textContent).toBe('1');
    expect(cells[3].textContent).toBe('2');
    expect(cells[4].textContent).toBe('3');
    expect(cells[5].textContent).toBe('4');
    expect(cells[6].textContent).toBe('5');
  });

  test("renders multiple weeks correctly", () => {
    const year = 2024;
    const month = 11;
    const days = [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
    const onSelectDay = vi.fn();
    
    const { container } = render(
      <Body year={year} month={month} days={days} onSelectDay={onSelectDay} />
    );
    
    const rows = container.querySelectorAll('tr');
    expect(rows).toHaveLength(3); // 3주치의 데이터이므로 3개의 행이 있어야 함
  });

  test("날짜 선택", async () => {
    const year = 2024;
    const month = 11;
    const days = [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
    const user = userEvent.setup();
    const onSelectDay = vi.fn();

    const { container } = render(
      <Body year={year} month={month} days={days} onSelectDay={onSelectDay} />
    );

    await user.click(container.querySelector('td[role="button"][role-label="day-1"]')!);
    expect(onSelectDay).toHaveBeenCalledWith(new Date(year, month - 1, 1));
  });
});

