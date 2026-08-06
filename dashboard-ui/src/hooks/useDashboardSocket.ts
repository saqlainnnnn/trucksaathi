import { useEffect } from "react";

import { DashboardSocket } from "../services/socket";
import { useDashboard } from "../store/dashboard";

export function useDashboardSocket() {
    const { handleEvent } = useDashboard();

    useEffect(() => {
        const socket = new DashboardSocket();

        socket.connect(handleEvent);

        return () => socket.disconnect();
    }, [handleEvent]);
}