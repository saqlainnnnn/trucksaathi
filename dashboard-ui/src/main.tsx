import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";
import { DashboardProvider } from "./store/dashboard";

import "./index.css";

ReactDOM.createRoot(
    document.getElementById("root")!,
).render(
    <React.StrictMode>
        <DashboardProvider>
            <App />
        </DashboardProvider>
    </React.StrictMode>,
);