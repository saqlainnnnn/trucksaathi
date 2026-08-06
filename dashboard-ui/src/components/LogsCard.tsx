import { useDashboard } from "../store/dashboard";

export default function LogsCard() {
    const { logs } = useDashboard();

    return (
        <div className="h-56 overflow-y-auto rounded-lg bg-black p-4 font-mono text-sm">
            <div className="space-y-2">
                {logs.map((log, index) => (
                    <div
                        key={index}
                        className="flex items-center gap-3"
                    >
                        <span className="text-zinc-500">
                            {log.time}
                        </span>

                        <span
                            className={
                                log.level === "success"
                                    ? "text-green-400"
                                    : log.level === "running"
                                    ? "text-yellow-400 animate-pulse"
                                    : log.level === "info"
                                    ? "text-blue-400"
                                    : "text-red-400"
                            }
                        >
                            {log.level === "success"
                                ? "✓"
                                : log.level === "running"
                                ? "●"
                                : log.level === "info"
                                ? "ℹ"
                                : "✕"}
                        </span>

                        <span className="text-zinc-200">
                            {log.message}
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
}