import { UID, StringTime } from "./base";
import { IPrice } from "./currency";

export interface ITimeslot {
    uid: UID;
    startTime: StringTime;
    endTime: StringTime;
    price: IPrice | null;
}
