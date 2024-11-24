import { beforeEach, describe, expect, test } from "vitest";
import { render } from "vitest-browser-react";
import Timeslots from "./Timeslots";
import { Timeslot } from "~/types/timeslot";

describe("Timeslots", () => {
    let date: Date | null = null;

    let mockTimeslots: Timeslot[] = [];

    beforeEach(() => {
        date = new Date();
        mockTimeslots = [
            {
                uid: "1",
                startTime: "09:00",
                endTime: "10:00",
                price: null,
            },
            {
                uid: 2,
                startTime: "14:00",
                endTime: "15:00",
                price: {
                    amount: 10000,
                    currency: "KRW",
                },
            }
        ];
    });

    test("타임슬롯이 없을 때 빈 상태 메시지 표시", async () => {
        const { container } = render(<Timeslots timeslots={[]} date={date} />);

        expect(container.querySelector('[role="status"][role-label="no-timeslots"]')).toHaveTextContent('예약 가능한 시간대가 없는 날입니다.');
    });

    test("타임슬롯 목록 렌더링", () => {
        const { container } = render(<Timeslots timeslots={mockTimeslots} date={date} />);

        const timeslotElements = container.querySelectorAll('[role="button"][role-label^="timeslot-"]');
        expect(timeslotElements).toHaveLength(2);

        // 첫 번째 타임슬롯 확인
        const firstTimeslot = container.querySelector('[role="button"][role-label="timeslot-1"]');
        expect(firstTimeslot).toHaveTextContent('09:00');

        // 두 번째 타임슬롯 확인
        const secondTimeslot = container.querySelector('[role="button"][role-label="timeslot-2"]');
        expect(secondTimeslot).toHaveTextContent('14:00');
        expect(secondTimeslot).toHaveTextContent('10000 KRW');
    });

    test("타임슬롯이 시간순으로 정렬되어 표시", () => {
        const unorderedTimeslots: Timeslot[] = [
            {
                uid: "1",
                startTime: "14:00",
                endTime: "15:00",
                price: null,
            },
            {
                uid: "2",
                startTime: "09:00",
                endTime: "10:00",
                price: null,
            }
        ];

        const { container } = render(<Timeslots timeslots={unorderedTimeslots} date={date} />);

        const timeslotElements = container.querySelectorAll('[role="button"][role-label^="timeslot-"]');
        const times = Array.from(timeslotElements).map(el =>
            el.querySelector('[role="time"]')?.textContent
        );

        expect(times).toEqual(['09:00', '14:00']);
    });
});
