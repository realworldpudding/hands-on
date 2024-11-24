
export interface IBooking {
    uid: UID;
    when: DateString;
    price: IPrice;
    timeslot: {
        uid: UID;
    };
}
