import { useDashboard } from "../store/dashboard";

export default function Pipeline() {
    const {
        pipeline,
        selectedStage,
        selectStage,
    } = useDashboard();

    return (
        <div className="flex flex-wrap items-center justify-center gap-4">
            {pipeline.map((stage) => (
                <button
                    key={stage.id}
                    onClick={() => selectStage(stage.id)}
                    className={`w-28 rounded-xl border p-4 transition-all duration-300 ${
                        selectedStage.id === stage.id
                            ? "border-blue-500 bg-zinc-800 shadow-lg shadow-blue-500/20"
                            : "border-zinc-700 hover:border-zinc-500 hover:bg-zinc-800"
                    }`}
                >
                    <div
                        className={`mx-auto mb-3 h-4 w-4 rounded-full ${
                            stage.status === "completed"
                                ? "bg-green-500"
                                : stage.status === "running"
                                ? "animate-pulse bg-yellow-400"
                                : stage.status === "failed"
                                ? "bg-red-500"
                                : "bg-zinc-600"
                        }`}
                    />

                    <p className="text-sm font-medium">
                        {stage.name}
                    </p>

                    <p className="mt-2 text-xs text-zinc-500">
                        {stage.latency
                            ? `${stage.latency} ms`
                            : "--"}
                    </p>
                </button>
            ))}
        </div>
    );
}