import bookingsData from '~/fixtures/bookings.json';
import { IBooking } from '~/types/booking';

export async function getBookings(year: number, month: number): Promise<IBooking[]> {
  await new Promise(resolve => setTimeout(resolve, 100)); // API 호출 시뮬레이션
  
  try {
    const yearData = bookingsData[year.toString() as keyof typeof bookingsData];
    if (!yearData) return [];
    
    const monthData = yearData[month.toString() as keyof typeof yearData];
    if (!monthData) return [];
    
    return monthData;
  } catch (error) {
    console.error('Failed to load bookings:', error);
    return [];
  }
}

export async function getBookingsByDate(date: { year: number; month: number }): Promise<IBooking[]> {
  const { year, month } = date;
  
  return await getBookings(year, month);
} 