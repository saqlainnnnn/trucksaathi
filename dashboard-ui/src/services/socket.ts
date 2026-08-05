export class DashboardSocket {
    connect() {
        console.log("Dashboard Connected");

        setInterval(() => {
            console.log({
                type: "stage_finished",
                stage: "stt",
                latency: Math.floor(
                    Math.random() * 1000,
                ),
            });
        }, 3000);
    }
    disconnect() {}

    send(_: unknown) {}
}