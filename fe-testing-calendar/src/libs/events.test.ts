import { describe, expect, test } from 'vitest';
import { getEventDetail } from './events';

describe('events', () => {
  test('getEventDetails returns event for specific date', async () => {
    const event = await getEventDetail('hannal-coffeechat');
    const keys = Object.keys(event || {});
    expect(keys).toEqual(["slug", "name", "description"]);
  });

  test('getEventDetails returns null for date without event', async () => {
    const event = await getEventDetail('test-slug');
    expect(event).toBeNull();
  });
}); 