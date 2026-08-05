import { request } from "../data/mock";

export default function Header() {
    return (
        <header className="flex items-center justify-between border-b border-zinc-800 pb-6">
            <div>
                <h1 className="text-5xl font-bold">
                    🚚 TruckSaathi Dashboard
                </h1>

                <p className="mt-2 text-zinc-500">
                    Live AI Pipeline Monitor
                </p>
            </div>

            <div className="flex gap-6">
                <Metric
                    title="Request"
                    value={request.id}
                />

                <Metric
                    title="Status"
                    value={request.status}
                />

                <Metric
                    title="Total"
                    value={request.totalLatency}
                />

                <Metric
                    title="Language"
                    value={request.language}
                />

                <div className="flex items-center gap-2 rounded-lg border border-zinc-700 px-4 py-3">
                    <div className="h-3 w-3 rounded-full bg-green-500 animate-pulse" />

                    <span>Connected</span>
                </div>
            </div>
        </header>
    );
}

interface MetricProps {
    title: string;
    value: string;
}

function Metric({
    title,
    value,
}: MetricProps) {
    return (
        <div className="rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3">
            <p className="text-xs uppercase tracking-wide text-zinc-500">
                {title}
            </p>

            <p className="mt-2 font-semibold">
                {value}
            </p>
        </div>
    );
}