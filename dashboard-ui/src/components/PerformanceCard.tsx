import { useDashboard } from "../store/dashboard";

export default function PerformanceCard() {
    const { pipeline } = useDashboard();

    const stages = pipeline.filter(
        (stage) => stage.latency !== undefined,
    );

    const maxLatency =
        stages.length > 0
            ? Math.max(
                  ...stages.map(
                      (stage) =>
                          stage.latency ?? 0,
                  ),
              )
            : 1;

    const total = stages.reduce(
        (sum, stage) =>
            sum + (stage.latency ?? 0),
        0,
    );

    return (
        <div className="space-y-5">
            {pipeline.map((stage) => (
                <div
                    key={stage.id}
                    className="grid grid-cols-[140px_1fr_70px] items-center gap-4"
                >
                    <span className="text-zinc-300">
                        {stage.name}
                    </span>

                    <div className="h-3 rounded-full bg-zinc-800">
                        <div
                            className="h-full rounded-full bg-blue-500 transition-all duration-500"
                            style={{
                                width:
                                    stage.latency !=
                                        null &&
                                    maxLatency > 0
                                        ? `${
                                              (stage.latency /
                                                  maxLatency) *
                                              100
                                          }%`
                                        : "0%",
                            }}
                        />
                    </div>

                    <span className="text-right text-sm text-zinc-400">
                        {stage.latency != null
                            ? `${stage.latency.toFixed(
                                  0,
                              )} ms`
                            : "--"}
                    </span>
                </div>
            ))}

            <div className="mt-8 border-t border-zinc-800 pt-5">
                <div className="flex justify-between text-lg font-semibold">
                    <span>Total</span>

                    <span>
                        {(total / 1000).toFixed(
                            2,
                        )}{" "}
                        s
                    </span>
                </div>
            </div>
        </div>
    );
}