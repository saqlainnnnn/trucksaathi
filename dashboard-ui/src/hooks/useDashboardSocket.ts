import { useEffect } from "react";

import { DashboardSocket } from "../services/socket";

export function useDashboardSocket() {
    useEffect(() => {
        const socket = new DashboardSocket();

        socket.connect();

        return () => socket.disconnect();
    }, []);
}