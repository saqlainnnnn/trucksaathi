from __future__ import annotations

from abc import ABC, abstractmethod

from schemas import BookingExtraction


class BookingRepository(ABC):
    """
    Abstract persistence interface for completed bookings.
    """

    @abstractmethod
    def save(
        self,
        booking: BookingExtraction,
    ) -> None:
        """
        Persist a completed booking.
        """
        raise NotImplementedError