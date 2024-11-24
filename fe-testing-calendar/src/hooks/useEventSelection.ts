import { useQueryClient } from '@tanstack/react-query';
import { getTimeslots } from '~/libs/timeslots';

export function useEventSelection() {
  const queryClient = useQueryClient();

  const handleSelectDay = async (date: Date) => {
    // 선택한 날짜의 상세 이벤트 데이터 가져오기
    await queryClient.prefetchQuery({
      queryKey: ['timeslots', date.toISOString()],
      queryFn: () => getTimeslots(date),
    });
  };

  return { handleSelectDay };
} 