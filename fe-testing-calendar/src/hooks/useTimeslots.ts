import { useQuery } from '@tanstack/react-query';
import { getTimeslots } from '~/libs/timeslots';
import { Timeslot } from '~/types/timeslot';

export function useTimeslots(date: Date | null) {
  return useQuery<Timeslot[]>({
    queryKey: ['timeslots', date?.toISOString()],
    queryFn: () => getTimeslots(date!),
    enabled: !!date, // date가 null이 아닐 때만 쿼리 실행
  });
} 