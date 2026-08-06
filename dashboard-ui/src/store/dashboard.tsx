import {
    createContext,
    useCallback,
    useContext,
    useState,
} from "react";

import {
    booking as initialBooking,
    conversation as initialConversation,
    logs as initialLogs,
    pipeline as initialPipeline,
} from "../data/mock";

import type {
    BookingState,
    ConversationMessage,
    LogEntry,
    PipelineStage,
    StageStatus,
} from "../types";

interface DashboardState {
    pipeline: PipelineStage[];
    selectedStage: PipelineStage;

    booking: BookingState;
    conversation: ConversationMessage[];
    logs: LogEntry[];

    selectStage: (id: string) => void;

    addLog: (log: LogEntry) => void;

    addConversation: (
        message: ConversationMessage,
    ) => void;

    updateBooking: <K extends keyof BookingState>(
        field: K,
        value: BookingState[K],
    ) => void;

    updateStage: (
        id: string,
        status: StageStatus,
        latency?: number,
    ) => void;

    handleEvent: (event: any) => void;
}

const DashboardContext =
    createContext<DashboardState | null>(null);

export function DashboardProvider({
    children,
}: {
    children: React.ReactNode;
}) {
    const [pipeline, setPipeline] =
        useState<PipelineStage[]>(
            initialPipeline,
        );

    const [selectedStage, setSelectedStage] =
        useState<PipelineStage>(
            initialPipeline[0]!,
        );

    const [booking, setBooking] =
        useState<BookingState>(
            initialBooking,
        );

    const [conversation, setConversation] =
        useState<
            ConversationMessage[]
        >(initialConversation);

    const [logs, setLogs] =
        useState<LogEntry[]>(initialLogs);

    const selectStage = useCallback(
        (id: string) => {
            const stage = pipeline.find(
                (s) => s.id === id,
            );

            if (stage) {
                setSelectedStage(stage);
            }
        },
        [pipeline],
    );

    const addLog = useCallback(
        (log: LogEntry) => {
            setLogs((prev) => [
                ...prev,
                log,
            ]);
        },
        [],
    );

    const addConversation =
        useCallback(
            (
                message: ConversationMessage,
            ) => {
                setConversation((prev) => [
                    ...prev,
                    message,
                ]);
            },
            [],
        );

    const updateBooking =
        useCallback(
            <
                K extends keyof BookingState,
            >(
                field: K,
                value: BookingState[K],
            ) => {
                setBooking((prev) => ({
                    ...prev,
                    [field]: value,
                }));
            },
            [],
        );

    const updateStage = useCallback(
        (
            id: string,
            status: StageStatus,
            latency?: number,
        ) => {
            setPipeline((prev) =>
                prev.map((stage) =>
                    stage.id === id
                        ? {
                              ...stage,
                              status,
                              latency:
                                  latency ??
                                  stage.latency,
                          }
                        : stage,
                ),
            );

            setSelectedStage((prev) =>
                prev.id === id
                    ? {
                          ...prev,
                          status,
                          latency:
                              latency ??
                              prev.latency,
                      }
                    : prev,
            );
        },
        [],
    );

    const handleEvent = useCallback(
        (event: any) => {
            switch (event.type) {
                case "stage_started":
                    updateStage(
                        event.payload.stage,
                        "running",
                    );
                    break;

                case "stage_finished":
                    updateStage(
                        event.payload.stage,
                        "completed",
                        event.payload.latency,
                    );
                    break;

                case "booking_updated":
                    setBooking(event.payload);
                    break;

                case "conversation":
                    addConversation({
                        role: event.payload.role,
                        text: event.payload.text,
                    });
                    break;

                case "log":
                    addLog({
                        time: new Date().toLocaleTimeString(),
                        level: event.payload.level,
                        message: event.payload.message,
                    });
                    break;

                default:
                    console.warn(
                        "Unknown dashboard event",
                        event,
                    );
            }
        },
        [
            addConversation,
            addLog,
            updateStage,
        ],
    );

    return (
        <DashboardContext.Provider
            value={{
                pipeline,
                selectedStage,

                booking,
                conversation,
                logs,

                selectStage,

                addLog,
                addConversation,

                updateBooking,
                updateStage,

                handleEvent,
            }}
        >
            {children}
        </DashboardContext.Provider>
    );
}

export function useDashboard() {
    const ctx =
        useContext(DashboardContext);

    if (!ctx) {
        throw new Error(
            "DashboardProvider missing.",
        );
    }

    return ctx;
}