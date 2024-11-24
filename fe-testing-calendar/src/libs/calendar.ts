export const getDaysInMonth = (date: Date) => {
    // 해당 월의 마지막 날짜를 구함
    return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
};

export const getCalendarDays = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const daysInMonth = getDaysInMonth(date);

    // 해당 월의 1일의 요일을 구함 (0: 일요일, 1: 월요일, ...)
    const firstDayOfMonth = new Date(year, month, 1).getDay();

    // 첫 주의 빈 날짜를 0으로 채움
    const days: number[] = Array(firstDayOfMonth).fill(0);

    // 실제 날짜 추가
    for (let day = 1; day <= daysInMonth; day++) {
        days.push(day);
    }

    // 마지막 주의 남은 칸을 0으로 채움 (7의 배수가 되도록)
    const remainingDays = 7 - (days.length % 7);
    if (remainingDays < 7) {
        days.push(...Array(remainingDays).fill(0));
    }

    return days;
};

