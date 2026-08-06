import type {
  BookingState,
  ConversationMessage,
  LogEntry,
  PipelineStage,
} from "../types";

export const pipeline: PipelineStage[] = [
    {
        id: "telegram_in",
        name: "Telegram",
        status: "idle",
    },
    {
        id: "ffmpeg",
        name: "FFmpeg",
        status: "idle",
    },
    {
        id: "stt",
        name: "STT",
        status: "idle",
    },
    {
        id: "extract",
        name: "Extraction",
        status: "idle",
    },
    {
        id: "merge",
        name: "Merge",
        status: "idle",
    },
    {
        id: "validation",
        name: "Validation",
        status: "idle",
    },
    {
        id: "followup",
        name: "Follow-up",
        status: "idle",
    },
    {
        id: "tts",
        name: "TTS",
        status: "idle",
    },
    {
        id: "telegram_out",
        name: "Reply",
        status: "idle",
    },
];

export const booking: BookingState = {
    pickup: "",
    destination: "",
    goods: "",
    weight: "",
    truck_type: "",
};

export const conversation: ConversationMessage[] =
    [];

export const logs: LogEntry[] = [];



