import clsx from "clsx";
import { IEvent } from "~/types/event";

interface NavigatorProps {
  event: IEvent;
  year: number;
  month: number;
  baseDate?: Date;
  onPrevious: (slug: string, date: { year: number; month: number }) => void;
  onNext: (slug: string, date: { year: number; month: number }) => void;
}

export default function Navigator({ event, year, month, baseDate, onPrevious, onNext }: NavigatorProps) {
  const now = baseDate ?? new Date();
  const isPast = year < now.getFullYear() || (year === now.getFullYear() && month <= now.getMonth() + 1);

  const handlePrevious = () => {
    if (month === 1) {
      onPrevious(event.slug, { year: year - 1, month: 12 });
    } else {
      onPrevious(event.slug, { year, month: month - 1 });
    }
  };

  const handleNext = () => {
    if (month === 12) {
      onNext(event.slug, { year: year + 1, month: 1 });
    } else {
      onNext(event.slug, { year, month: month + 1 });
    }
  };

  return (
    <div className={clsx("w-full flex justify-center items-center space-x-5")}>
      <NavigatorButton
        role="button"
        role-label="button-이전달"
        disabled={isPast}
        onClick={handlePrevious}
      >
        &lt;
      </NavigatorButton>

      <h3 role="label" role-label="year-month" className="text-xl font-semibold">{year}년 {month}월</h3>

      <NavigatorButton
        role="button"
        role-label="button-다음달"
        onClick={handleNext}
      >
        &gt;
      </NavigatorButton>
    </div>
  );
}

function NavigatorButton(props: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      className={clsx(
        "text-primary hover:text-white hover:bg-primary font-bold rounded-full w-8 h-8 select-none flex items-center justify-center",
        {'cursor-default text-gray-500 hover:text-gray-500 hover:bg-inherit hover:border-transparent': props.disabled}
      )}
      {...props}
    />
  );
}
