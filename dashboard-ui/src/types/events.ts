export type DashboardEvent =
    | StageStartedEvent
    | StageFinishedEvent
    | LogEvent
    | ConversationEvent
    | BookingEvent;

export interface StageStartedEvent {
    type: "stage_started";
    stage: string;
}

export interface StageFinishedEvent {
    type: "stage_finished";
    stage: string;
    latency: number;
}

export interface LogEvent {
    type: "log";
    level: "success" | "running" | "error";
    message: string;
}

export interface ConversationEvent {
    type: "conversation";
    role: "user" | "assistant";
    text: string;
}

export interface BookingEvent {
    type: "booking";
    field: string;
    value: string;
}