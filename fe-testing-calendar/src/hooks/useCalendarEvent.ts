import { useQuery } from '@tanstack/react-query';
import { getEventDetail } from '~/libs/events';
import { IEvent } from '~/types/event';

export function useCalendarEvent(slug: string) {
  const { data: event } = useQuery<IEvent | null>({
    queryKey: ['slug', slug],
    queryFn: () => getEventDetail(slug),
  });

  return event ?? null;
} 
