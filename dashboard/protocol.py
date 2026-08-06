from __future__ import annotations

from pathlib import Path
from typing import Protocol

from schemas import BookingExtraction


class DashboardEmitterProtocol(Protocol):

    async def stage_started(
        self,
        stage: str,
    ) -> None: ...

    async def stage_finished(
        self,
        stage: str,
        latency_ms: float,
    ) -> None: ...

    async def log(
        self,
        message: str,
    ) -> None: ...

    async def transcript(
        self,
        text: str,
    ) -> None: ...

    async def booking(
        self,
        booking: BookingExtraction,
    ) -> None: ...