from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class DashboardEvent:
    event_type: str
    payload: dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    id: int | None = None