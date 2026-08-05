import type {
  BookingState,
  ConversationMessage,
  LogEntry,
  PipelineStage,
} from "../types";

export const pipeline: PipelineStage[] = [
  { id: "telegram_in", name: "Telegram", status: "completed", latency: 81 },
  { id: "ffmpeg", name: "FFmpeg", status: "completed", latency: 24 },
  { id: "stt", name: "STT", status: "completed", latency: 812 },
  { id: "extract", name: "Extraction", status: "completed", latency: 421 },
  { id: "merge", name: "Merge", status: "completed", latency: 1 },
  { id: "validation", name: "Validation", status: "completed", latency: 0 },
  { id: "followup", name: "Follow-up", status: "running" },
  { id: "tts", name: "TTS", status: "idle" },
  { id: "telegram_out", name: "Reply", status: "idle" },
];

export const booking: BookingState = {
  pickup: "Pune",
  destination: "Hyderabad",
  goods: "Cement",
  weight: "12 Ton",
  truck_type: "Large Truck",
};

export const conversation: ConversationMessage[] = [
  {
    role: "user",
    text: "Pune se Hyderabad truck chahiye.",
  },
  {
    role: "assistant",
    text: "Truck ka type kya hoga?",
  },
];

export const logs: LogEntry[] = [
    {
        time: "18:42:11",
        level: "success",
        message: "Telegram update received",
    },
    {
        time: "18:42:11",
        level: "success",
        message: "Downloaded voice note",
    },
    {
        time: "18:42:11",
        level: "success",
        message: "Converted OGG → WAV",
    },
    {
        time: "18:42:12",
        level: "success",
        message: "Speech transcription completed",
    },
    {
        time: "18:42:12",
        level: "success",
        message: "Booking extracted",
    },
    {
        time: "18:42:12",
        level: "success",
        message: "Merge completed",
    },
    {
        time: "18:42:13",
        level: "running",
        message: "Generating follow-up",
    },
];

export const performance = [
    {
        stage: "Telegram",
        latency: 81,
    },
    {
        stage: "FFmpeg",
        latency: 24,
    },
    {
        stage: "STT",
        latency: 812,
    },
    {
        stage: "Extraction",
        latency: 421,
    },
    {
        stage: "Merge",
        latency: 1,
    },
    {
        stage: "Validation",
        latency: 0,
    },
    {
        stage: "Follow-up",
        latency: 311,
    },
    {
        stage: "TTS",
        latency: 602,
    },
];

export const request = {
    id: "20260805_3bc5ee71",
    status: "Running",
    language: "Hindi",
    totalLatency: "2.25 s",
};

