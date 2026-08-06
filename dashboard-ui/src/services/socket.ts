export class DashboardSocket {
    private socket: WebSocket | null = null;

    connect(
        onMessage: (event: any) => void,
    ) {
        this.socket = new WebSocket(
            "ws://127.0.0.1:8000/ws",
        );

        this.socket.onopen = () => {
            console.log(
                "✅ Dashboard Connected",
            );
        };

        this.socket.onmessage = (
            event,
        ) => {
            const data = JSON.parse(
                event.data,
            );

            console.log(data);

            onMessage(data);
        };

        this.socket.onerror = (
            error,
        ) => {
            console.error(error);
        };

        this.socket.onclose = () => {
            console.log(
                "Dashboard Disconnected",
            );
        };
    }

    disconnect() {
        this.socket?.close();
    }

    send(data: unknown) {
        this.socket?.send(
            JSON.stringify(data),
        );
    }
}