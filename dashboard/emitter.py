from __future__ import annotations

import asyncio
from dataclasses import asdict
from typing import Any

from dashboard.models import DashboardEvent


class DashboardEmitter:
    """
    Async event queue consumed by the dashboard.

    Every backend component emits high-level events here.
    The websocket server simply forwards them to the frontend.
    """

    def __init__(self) -> None:
        self._queue: asyncio.Queue[DashboardEvent] = (
            asyncio.Queue()
        )

    async def emit(
        self,
        event: DashboardEvent,
    ) -> None:
        await self._queue.put(event)

    async def next_event(
        self,
    ) -> DashboardEvent:
        return await self._queue.get()

    async def stage_started(
        self,
        stage: str,
    ) -> None:
        await self.emit(
            DashboardEvent(
                type="stage_started",
                payload={
                    "stage": stage,
                },
            )
        )

    async def stage_finished(
        self,
        stage: str,
        latency_ms: float,
    ) -> None:
        await self.emit(
            DashboardEvent(
                type="stage_finished",
                payload={
                    "stage": stage,
                    "latency": round(latency_ms, 2),
                },
            )
        )

    async def log(
        self,
        message: str,
        level: str = "success",
    ) -> None:
        await self.emit(
            DashboardEvent(
                type="log",
                payload={
                    "level": level,
                    "message": message,
                },
            )
        )

    async def transcript(
        self,
        text: str,
    ) -> None:
        await self.emit(
            DashboardEvent(
                type="conversation",
                payload={
                    "role": "user",
                    "text": text,
                },
            )
        )

    async def assistant_reply(
        self,
        text: str,
    ) -> None:
        await self.emit(
            DashboardEvent(
                type="conversation",
                payload={
                    "role": "assistant",
                    "text": text,
                },
            )
        )

    async def booking(
        self,
        booking: Any,
    ) -> None:
        """
        Emits the latest booking state.

        Works with dataclasses or Pydantic models.
        """

        if hasattr(booking, "model_dump"):
            payload = booking.model_dump()

        elif hasattr(booking, "__dataclass_fields__"):
            payload = asdict(booking)

        else:
            payload = dict(booking)

        await self.emit(
            DashboardEvent(
                type="booking",
                payload=payload,
            )
        )


dashboard = DashboardEmitter()