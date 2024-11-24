import eventsData from '~/fixtures/events.json';
import { IEvent } from '~/types/event';

export async function getEventDetail(slug: string): Promise<IEvent | null> {
  return Promise.resolve(eventsData.find(event => event.slug === slug) as IEvent ?? null);
} 
