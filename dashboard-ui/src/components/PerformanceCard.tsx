import { performance } from "../data/mock";

export default function PerformanceCard() {
    const maxLatency = Math.max(
        ...performance.map((s) => s.latency),
    );

    const total = performance.reduce(
        (sum, stage) => sum + stage.latency,
        0,
    );

    return (
        <div className="space-y-5">
            {performance.map((stage) => (
                <div
                    key={stage.stage}
                    className="grid grid-cols-[140px_1fr_70px] items-center gap-4"
                >
                    <span className="text-zinc-300">
                        {stage.stage}
                    </span>

                    <div className="h-3 rounded-full bg-zinc-800">
                        <div
                            className="h-full rounded-full bg-blue-500 transition-all duration-500"
                            style={{
                                width: `${
                                    (stage.latency /
                                        maxLatency) *
                                    100
                                }%`,
                            }}
                        />
                    </div>

                    <span className="text-right text-sm text-zinc-400">
                        {stage.latency} ms
                    </span>
                </div>
            ))}

            <div className="mt-8 border-t border-zinc-800 pt-5">
                <div className="flex justify-between text-lg font-semibold">
                    <span>Total</span>

                    <span>
                        {(total / 1000).toFixed(2)} s
                    </span>
                </div>
            </div>
        </div>
    );
}