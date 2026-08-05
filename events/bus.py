from __future__ import annotations

from collections.abc import Callable

from events.models import DashboardEvent

Subscriber = Callable[[DashboardEvent], None]


class EventBus:

    def __init__(self):
        self._subscribers = []

    def subscribe(self, fn: Subscriber):
        self._subscribers.append(fn)

    def emit(self, event: DashboardEvent):
        for subscriber in self._subscribers:
            subscriber(event)


event_bus = EventBus()