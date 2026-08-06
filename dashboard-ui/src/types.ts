export type StageStatus =
    | "idle"
    | "running"
    | "completed"
    | "failed";

export interface PipelineStage {
    id: string;
    name: string;
    status: StageStatus;
    latency?: number;
}

export interface BookingState {
    pickup?: string;
    destination?: string;
    truck_type?: string;
    goods?: string;
    weight?: string;
    pickup_date?: string;
    pickup_time?: string;
    contact_name?: string;
    phone_number?: string;
}

export interface ConversationMessage {
    role: "user" | "assistant";
    text: string;
    time?: string;
}

export interface LogEntry {
    time: string;
    level:
        | "success"
        | "running"
        | "info"
        | "error";
    message: string;
}