from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from dashboard.models import DashboardEvent


class DashboardRepository(ABC):

    @abstractmethod
    def save(
        self,
        event: DashboardEvent,
    ) -> DashboardEvent:
        ...

    @abstractmethod
    def get_after(
        self,
        event_id: int,
    ) -> list[DashboardEvent]:
        ...

    @abstractmethod
    def log(
        self,
        message: str,
        level: str = "info",
    ) -> None:
        ...

    @abstractmethod
    def stage_started(
        self,
        stage: str,
    ) -> None:
        ...

    @abstractmethod
    def stage_finished(
        self,
        stage: str,
        latency_ms: float,
    ) -> None:
        ...