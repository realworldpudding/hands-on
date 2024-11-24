
export interface IEvent {
    slug: string;
    name: string;
    summary?: string;
    description?: string;
    product_description?: string;
    contents?: string;
    note?: string;
    extra: IEventExtraSchema;
    price: Price;
    participation_count: number;
    kind: EnumEventKind;
    is_public: boolean;
    started_at: ISO8601String;
    closed_at: ISO8601String | null;
}

export enum EnumEventKind {
    COFFEECHAT = "coffeechat",
    STUDYCAMP = "studycamp",
    TOYSTORY = "toystory",
    WRITING = "writing",
    CONFERENCE = "conference",
    SEMINAR = "seminar",
    MEETUP = "meetup",
    WORKSHOP = "workshop",
}

export interface IEventExtraSchema {
    og_image_url_intro?: string | null;
    og_image_url_list?: string | null;
    og_image_url_speakers?: string | null;
    og_image_url_participants?: string | null;
    og_image_url_contents?: string | null;
    og_image_url_questions?: string | null;
    og_image_url_sponsors?: string | null;
    og_image_url_staffs?: string | null;
}       