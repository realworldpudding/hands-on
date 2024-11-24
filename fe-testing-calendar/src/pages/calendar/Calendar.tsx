import clsx from 'clsx';

import { useSearch, useParams } from '@tanstack/react-router';
import { useState } from 'react';

import { Body, BookingForm, Navigator, Timeslots } from '~/components/calendar'
import { getCalendarDays } from '~/libs/calendar';
import { useCalendarEvent } from '~/hooks/useCalendarEvent';
import { useCalendarNavigation } from '~/hooks/useCalendarNavigation';
import { useEventSelection } from '~/hooks/useEventSelection';
import { useTimeslots } from '~/hooks/useTimeslots';
import { ITimeslot } from '~/types/timeslot';

import './calendar.less';

function Calendar({ baseDate }: { baseDate?: Date }) {
  const { year, month } = useSearch({ from: '/calendar/$slug' });
  const { slug } = useParams({ from: '/calendar/$slug' });
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [selectedTimeslot, setSelectedTimeslot] = useState<ITimeslot | null>(null);
  
  const event = useCalendarEvent(slug);
  const { data: timeslots = [] } = useTimeslots(selectedDate);
  const { handlePrevious, handleNext } = useCalendarNavigation();
  const { handleSelectDay } = useEventSelection();

  const handleDaySelect = (date: Date) => {
    setSelectedDate(date);
    handleSelectDay(date);
  };

  const handleSelectTimeslot = (timeslot: ITimeslot) => {
    setSelectedTimeslot(timeslot);
  };

  if(!event) return null;
  
  return (
    <div className={clsx("flex flex-col w-full space-y-8")}>
      <h2 className="text-2xl font-bold">{event.name}</h2>
      
      <Navigator
        event={event}
        year={year}
        month={month}
        baseDate={baseDate}
        onPrevious={handlePrevious}
        onNext={handleNext}
      />

      <div className={clsx("flex flex-row gap-4")}>
        <Body
          year={year}
          month={month}
          days={getCalendarDays(new Date(year, month - 1))}
          baseDate={baseDate}
          onSelectDay={handleDaySelect}
        />
        <BookingForm timeslot={selectedTimeslot} event={event} />
        <Timeslots timeslots={timeslots} date={selectedDate} onSelectTimeslot={handleSelectTimeslot} />
      </div>
 
    </div>
    
  );
}

export default Calendar;
