from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class DashboardEvent:
    event: str
    timestamp: float
    data: dict[str, Any]