import {
    createContext,
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
}

const DashboardContext =
    createContext<DashboardState | null>(null);

export function DashboardProvider({
    children,
}: {
    children: React.ReactNode;
}) {
    const [pipeline, setPipeline] =
        useState<PipelineStage[]>(initialPipeline);

    const [selectedStage, setSelectedStage] =
        useState<PipelineStage>(initialPipeline[0]!);

    const [booking, setBooking] =
        useState<BookingState>(initialBooking);

    const [conversation, setConversation] =
        useState<ConversationMessage[]>(
            initialConversation,
        );

    const [logs, setLogs] =
        useState<LogEntry[]>(initialLogs);

    function selectStage(id: string) {
        const stage = pipeline.find(
            (s) => s.id === id,
        );

        if (stage) {
            setSelectedStage(stage);
        }
    }

    function addLog(log: LogEntry) {
        setLogs((prev) => [...prev, log]);
    }

    function addConversation(
        message: ConversationMessage,
    ) {
        setConversation((prev) => [
            ...prev,
            message,
        ]);
    }

    function updateBooking<
        K extends keyof BookingState,
    >(
        field: K,
        value: BookingState[K],
    ) {
        setBooking((prev) => ({
            ...prev,
            [field]: value,
        }));
    }

    function updateStage(
        id: string,
        status: StageStatus,
        latency?: number,
    ) {
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

        if (selectedStage.id === id) {
            setSelectedStage((prev) => ({
                ...prev,
                status,
                latency:
                    latency ??
                    prev.latency,
            }));
        }
    }

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