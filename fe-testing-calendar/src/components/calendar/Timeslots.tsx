import clsx from "clsx";

import { Button } from "~/components/button";
import { Timeslot } from "~/types/timeslot";

interface TimeslotsProps {
    date: Date | null;
    timeslots: Timeslot[];
    onSelectTimeslot: (timeslot: Timeslot) => void;
}

export default function Timeslots({ date, timeslots, onSelectTimeslot }: TimeslotsProps) {
    return <div className={clsx("flex flex-col gap-2")}>
        {timeslots.length === 0 && !date && (
            <div
                role="status"
                role-label="no-date"
                className="space-y-3 md:space-y-4 w-full md:w-60 md:min-w-60 text-center md:w-full md:text-left">
                <p>커피챗을 신청할 날짜를 고르세요.</p>
                <p className="text-sm">커피챗이 정상 동작하지 않을 경우 `hannal@puddingcamp.com`로 커피챗을 수동 신청하며 제보해주세요.</p>
                <a
                    href="{{ url('page-login') }}?next-to={{ url('event-coffeechat-index', event_slug=event.slug) }}"
                    className="block w-full border border-blue-100 font-semibold rounded py-3 text-center bg-primary text-white hover:bg-secondary">
                  로그인 후 커피챗 신청하기
                </a>
            </div>
        )}

        {timeslots.length === 0 && !!date && (<div role="status" role-label="no-timeslots">
                <p>예약 가능한 시간대가 없는 날입니다.</p>
            </div>
        )}

        {timeslots.sort((a, b) => a.startTime.localeCompare(b.startTime)).map((timeslot) => (
            <Button
                variant="secondary"
                type="button"
                role="button"
                role-label={`timeslot-${timeslot.uid}`}
                key={timeslot.uid}
                className={clsx("w-full h-10 rounded-md border border-gray-200")}
                onClick={() => onSelectTimeslot(timeslot)}
            >
                <span role="time">{timeslot.startTime}</span>
                {timeslot.price && <span role="price">{timeslot.price.amount} {timeslot.price.currency}</span>}
            </Button>
        ))}
    </div>
}
