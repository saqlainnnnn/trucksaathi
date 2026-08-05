import Header from "./components/Header";
import Pipeline from "./components/Pipeline";
import StageDetails from "./components/StageDetails";
import BookingCard from "./components/BookingCard";
import ConversationCard from "./components/ConversationCard";
import PerformanceCard from "./components/PerformanceCard";
import LogsCard from "./components/LogsCard";
import { useDashboardSocket } from "./hooks/useDashboardSocket";

export default function App() {
    useDashboardSocket();
    return (
        <div className="min-h-screen bg-zinc-950 text-white">
            <main className="mx-auto flex max-w-7xl flex-col gap-6 p-8">
                <Header />

                <section className="grid gap-6 lg:grid-cols-3">
                    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6 lg:col-span-2">
                        <h2 className="mb-6 text-xl font-semibold">
                            Pipeline
                        </h2>

                        <Pipeline />
                    </div>

                    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
                        <h2 className="mb-6 text-xl font-semibold">
                            Stage Details
                        </h2>

                        <StageDetails />
                    </div>
                </section>

                <section className="grid gap-6 lg:grid-cols-2">
                    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
                        <h2 className="mb-4 text-xl font-semibold">
                            Booking State
                        </h2>

                        <BookingCard />
                    </div>

                    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
                        <h2 className="mb-4 text-xl font-semibold">
                            <ConversationCard />
                        </h2>

                        <BookingCard />
                    </div>
                </section>

                <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
                    <h2 className="mb-4 text-xl font-semibold">
                        Performance
                    </h2>

                    <PerformanceCard />
                </section>

                <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
                    <h2 className="mb-4 text-xl font-semibold">
                        Live Logs
                    </h2>

                        <LogsCard />
                </section>
            </main>
        </div>
    );
}