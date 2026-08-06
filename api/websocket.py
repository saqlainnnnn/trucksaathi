from __future__ import annotations

import asyncio

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from config import settings
from dashboard.sqlite_repository import (
    SQLiteDashboardRepository,
)

router = APIRouter()

repository = SQLiteDashboardRepository(
    settings.database_path,
)


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
):
    print(">>> Incoming websocket")

    await websocket.accept()

    print(">>> Accepted websocket")

    last_seen = 0

    try:
        while True:

            events = repository.get_after(
                last_seen,
            )

            if events:
                print(f">>> Sending {len(events)} events")

            for event in events:

                await websocket.send_json(
                    {
                        "id": event.id,
                        "type": event.event_type,
                        "payload": event.payload,
                    }
                )

                last_seen = event.id

            await asyncio.sleep(0.1)

    except WebSocketDisconnect:
        print(">>> Client disconnected")