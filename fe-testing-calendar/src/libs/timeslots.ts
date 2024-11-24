import timeslotsData from '~/fixtures/timeslots.json';
import { Timeslot } from '~/types/timeslot';

export async function getTimeslots(date: Date): Promise<Timeslot[]> {
  await new Promise(resolve => setTimeout(resolve, 100)); // API 호출 시뮬레이션
  
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  
  try {
    const yearData = timeslotsData[year as unknown as keyof typeof timeslotsData];
    if (!yearData) return [];
    
    const monthData = yearData[month as unknown as keyof typeof yearData];
    if (!monthData) return [];
    
    const dayData = monthData[day as unknown as keyof typeof monthData];
    if (!dayData) return [];
    
    return dayData;
  } catch (error) {
    console.error('Failed to load timeslots:', error);
    return [];
  }
} 