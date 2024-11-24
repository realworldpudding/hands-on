import clsx from "clsx";

interface BodyProps {
    year: number;
    month: number;
    days: number[];
    baseDate?: Date;
    onSelectDay: (date: Date) => void;
}

export default function Body({ year, month, days, baseDate, onSelectDay }: BodyProps) {
  // 7일씩 나누어 2차원 배열로 변환
  const weeks = days.reduce<number[][]>((acc, day, i) => {
    const weekIndex = Math.floor(i / 7);
    
    if (!acc[weekIndex]) {
      acc[weekIndex] = [];
    }
    
    acc[weekIndex].push(day);
    return acc;
  }, []);

  const now = baseDate ?? new Date();

  return (
    <div className={clsx("w-full h-full md:w-[470px] md:h-[390px]")}>
      <table
        className={clsx("w-full h-full")}
      >
        <thead className="w-full">
          <tr className="text-lg font-semibold border-b grid grid-cols-7 gap-4">
            <th className="text-center text-red-500">일</th>
            <th className="text-center">월</th>
            <th className="text-center">화</th>
            <th className="text-center">수</th>
            <th className="text-center">목</th>
            <th className="text-center">금</th>
            <th className="text-center text-blue-500">토</th>
          </tr>
        </thead>

        <tbody role="grid" role-label="calendar-body" className="w-full">
          {weeks.map((week, weekIndex) => (
            <tr key={weekIndex} className="grid grid-cols-7 gap-4">
              {week.map((day, dayIndex) => {
                const isUnavailable = (dayIndex % 7 === 0 || dayIndex % 7 === 6)
                  || (year < now.getFullYear() || (year === now.getFullYear() && month < now.getMonth() + 1))
                  || (year === now.getFullYear() && month === now.getMonth() + 1 && day < now.getDate());
                const isAvailable = !isUnavailable && day !== 0;

                return (
                <td
                  role={day !== 0 ? "button" : undefined}
                  role-label={day !== 0 ? `day-${day}` : undefined}
                  key={dayIndex}
                  className={clsx(
                    "booking-cell flex justify-center items-center rounded-full w-12 h-12 select-none",
                    {'text-sm text-[#AAAAAA] bg-inherit hover:cursor-default': isUnavailable},
                    {'text-lg font-bold text-primary bg-blue-50': isAvailable},
                    {'cursor-pointer hover:bg-primary hover:text-white': isAvailable},
                  )}
                  onClick={() => onSelectDay(new Date(year, month - 1, day))}
                >
                  {day !== 0 && day}
                </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
