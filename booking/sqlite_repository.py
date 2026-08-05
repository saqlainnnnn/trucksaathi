from __future__ import annotations

import sqlite3
from pathlib import Path

from booking.repository import BookingRepository
from schemas import BookingExtraction


class SQLiteBookingRepository(BookingRepository):
    """
    SQLite-backed repository for completed bookings.
    """

    def __init__(
        self,
        database_path: str | Path,
    ) -> None:
        self._database_path = Path(database_path)

        self._database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._connection = sqlite3.connect(
            self._database_path,
        )

        self._connection.row_factory = sqlite3.Row

        self._create_schema()

    def _create_schema(self) -> None:
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS completed_bookings (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                created_at TEXT DEFAULT CURRENT_TIMESTAMP,

                pickup TEXT,
                destination TEXT,
                truck_type TEXT,
                goods TEXT,
                weight TEXT,
                pickup_date TEXT,
                pickup_time TEXT,
                contact_name TEXT,
                phone_number TEXT

            );
            """
        )

        self._connection.commit()

    def save(
        self,
        booking: BookingExtraction,
    ) -> None:
        self._connection.execute(
            """
            INSERT INTO completed_bookings (

                pickup,
                destination,
                truck_type,
                goods,
                weight,
                pickup_date,
                pickup_time,
                contact_name,
                phone_number

            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                booking.pickup.value,
                booking.destination.value,
                booking.truck_type.value,
                booking.goods.value,
                booking.weight.value,
                booking.pickup_date.value,
                booking.pickup_time.value,
                booking.contact_name.value,
                booking.phone_number.value,
            ),
        )

        self._connection.commit()

    def close(self) -> None:
        self._connection.close()