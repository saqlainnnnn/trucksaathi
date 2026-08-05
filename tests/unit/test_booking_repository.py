from booking.sqlite_repository import SQLiteBookingRepository
from schemas import BookingExtraction, BookingField


def test_booking_repository_save(tmp_path):
    database = tmp_path / "trucksaathi.db"

    repository = SQLiteBookingRepository(database)

    booking = BookingExtraction(
        pickup=BookingField(value="Mumbai"),
        destination=BookingField(value="Pune"),
    )

    repository.save(booking)

    cursor = repository._connection.execute(
        "SELECT COUNT(*) FROM completed_bookings"
    )

    count = cursor.fetchone()[0]

    assert count == 1

    repository.close()