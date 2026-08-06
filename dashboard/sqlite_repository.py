from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from dashboard.models import DashboardEvent
from dashboard.repository import DashboardRepository


class SQLiteDashboardRepository(
    DashboardRepository,
):
    def __init__(
        self,
        database_path: str,
    ) -> None:

        self._connection = sqlite3.connect(
            database_path,
            check_same_thread=False,
        )

        self._connection.row_factory = (
            sqlite3.Row
        )

        self._create_table()

    def _create_table(self) -> None:

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS dashboard_events(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                timestamp TEXT NOT NULL,

                event_type TEXT NOT NULL,

                payload TEXT NOT NULL
            )
            """
        )

        self._connection.commit()

    def save(
        self,
        event: DashboardEvent,
    ) -> DashboardEvent:

        cursor = self._connection.execute(
            """
            INSERT INTO dashboard_events(
                timestamp,
                event_type,
                payload
            )
            VALUES(
                ?,
                ?,
                ?
            )
            """,
            (
                event.timestamp.isoformat(),
                event.event_type,
                json.dumps(event.payload),
            ),
        )

        self._connection.commit()

        event.id = cursor.lastrowid

        return event

    def get_after(
        self,
        event_id: int,
    ) -> list[DashboardEvent]:

        rows = self._connection.execute(
            """
            SELECT *
            FROM dashboard_events
            WHERE id > ?
            ORDER BY id
            """,
            (
                event_id,
            ),
        ).fetchall()

        return [
            DashboardEvent(
                id=row["id"],
                timestamp=datetime.fromisoformat(
                    row["timestamp"],
                ),
                event_type=row["event_type"],
                payload=json.loads(
                    row["payload"],
                ),
            )
            for row in rows
        ]

    def log(
        self,
        message: str,
        level: str = "info",
    ) -> None:

        self.save(
            DashboardEvent(
                event_type="log",
                payload={
                    "level": level,
                    "message": message,
                },
                timestamp=datetime.utcnow(),
            )
        )


    def stage_started(
        self,
        stage: str,
    ) -> None:

        self.save(
            DashboardEvent(
                event_type="stage_started",
                payload={
                    "stage": stage,
                },
                timestamp=datetime.utcnow(),
            )
        )


    def stage_finished(
        self,
        stage: str,
        latency_ms: float,
    ) -> None:

        self.save(
            DashboardEvent(
                event_type="stage_finished",
                payload={
                    "stage": stage,
                    "latency": latency_ms,
                },
                timestamp=datetime.utcnow(),
            )
        )

    def close(self) -> None:
        self._connection.close()