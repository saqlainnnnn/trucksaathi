import { useDashboard } from "../store/dashboard";

export default function StageDetails() {
    const { selectedStage } = useDashboard();

    return (
        <div className="space-y-6">
            <div>
                <p className="text-sm text-zinc-500">
                    Selected Stage
                </p>

                <h3 className="mt-2 text-2xl font-bold">
                    {selectedStage.name}
                </h3>
            </div>

            <div>
                <p className="text-sm text-zinc-500">
                    Status
                </p>

                <p className="mt-2 capitalize">
                    {selectedStage.status}
                </p>
            </div>

            <div>
                <p className="text-sm text-zinc-500">
                    Latency
                </p>

                <p className="mt-2 text-lg">
                    {selectedStage.latency
                        ? `${selectedStage.latency} ms`
                        : "--"}
                </p>
            </div>

            <div>
                <p className="text-sm text-zinc-500">
                    Stage ID
                </p>

                <div className="mt-2 rounded-lg bg-zinc-950 p-3 font-mono text-xs">
                    {selectedStage.id}
                </div>
            </div>
        </div>
    );
}