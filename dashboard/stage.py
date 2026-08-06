from __future__ import annotations

import time
from contextlib import contextmanager

from dashboard.repository import DashboardRepository


@contextmanager
def dashboard_stage(
    dashboard: DashboardRepository,
    stage: str,
):
    dashboard.stage_started(stage)

    start = time.perf_counter()

    try:
        yield

    finally:
        dashboard.stage_finished(
            stage,
            (time.perf_counter() - start)
            * 1000,
        )