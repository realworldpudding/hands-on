import { beforeAll, describe, expect, test, vi } from "vitest";
import { render } from "vitest-browser-react";
import userEvent from "@testing-library/user-event";
import Navigator from "~/components/calendar/Navigator";
import { IEvent } from "~/types/event";

describe("Navigator", () => {
  let event: IEvent;
  let baseDate: Date;
  let nextYearDate: Date;

  beforeAll(() => {
    event = { slug: "test", name: "test" } as IEvent;
    baseDate = new Date();
    nextYearDate = new Date(baseDate.getFullYear() + 1, baseDate.getMonth(), baseDate.getDate());
  });
  
  test("일반적인 경우의 이전/다음 달 이동", async () => {
    const user = userEvent.setup();
    const onPrevious = vi.fn();
    const onNext = vi.fn();
    
    const { container } = render(
      <Navigator 
        event={event}
        year={baseDate.getFullYear()} 
        month={baseDate.getMonth() + 1 + 1} 
        baseDate={baseDate}
        onPrevious={onPrevious} 
        onNext={onNext} 
      />
    );

    // 이전 버튼 클릭 (12월 -> 11월)
    await user.click(container.querySelector('button[role="button"][role-label="button-이전달"]')!);
    expect(onPrevious).toHaveBeenCalledWith(event.slug, { year: 2024, month: 11 });

    // 다음 버튼 클릭 (12월 -> 1월)
    await user.click(container.querySelector('button[role="button"][role-label="button-다음달"]')!);
    expect(onNext).toHaveBeenCalledWith(event.slug, { year: 2025, month: 1 });
  });

  test("과거로 이동 불가", async () => {
    const user = userEvent.setup();
    const onPrevious = vi.fn();
    const onNext = vi.fn();
    const now = new Date();

    const { container } = render(
      <Navigator 
        event={event}
        year={now.getFullYear()} 
        month={now.getMonth() + 1} 
        onPrevious={onPrevious} 
        onNext={onNext} 
      />
    );

    await user.click(container.querySelector('button[role="button"][role-label="button-이전달"]')!);
    expect(onPrevious).not.toHaveBeenCalled();
  });

  test("연도가 바뀌는 경우", async () => {
    const user = userEvent.setup();
    const onPrevious = vi.fn();
    const onNext = vi.fn();
    
    // 1월의 경우
    const { container } = render(
      <Navigator 
        event={event}
        year={nextYearDate.getFullYear()} 
        month={1} 
        baseDate={baseDate}
        onPrevious={onPrevious} 
        onNext={onNext} 
      />
    );

    await user.click(container.querySelector('button[role="button"][role-label="button-이전달"]')!);
    expect(onPrevious).toHaveBeenCalledWith(event.slug, { year: baseDate.getFullYear(), month: 12 });

    // 12월의 경우
    const { container: container2 } = render(
      <Navigator 
        event={event}
        year={baseDate.getFullYear()} 
        month={12} 
        baseDate={baseDate}
        onPrevious={onPrevious} 
        onNext={onNext} 
      />
    );

    await user.click(container2.querySelector('button[role="button"][role-label="button-다음달"]')!);
    expect(onNext).toHaveBeenCalledWith(event.slug, { year: nextYearDate.getFullYear(), month: 1 });
  });
}); 