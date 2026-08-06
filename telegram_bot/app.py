from __future__ import annotations

from booking.sqlite_repository import SQLiteBookingRepository
from config import settings
from conversation.manager import ConversationManager
from conversation.merge import MergeEngine
from conversation.sqlite_store import SQLiteSessionStore
from dashboard.sqlite_repository import (
    SQLiteDashboardRepository,
)
from llm.extractor import extract_booking
from llm.followup import generate_followup
from speech.stt import transcribe
from speech.tts import (
    synthesize_confirmation,
    synthesize_followup,
)
from validation.validator import validate_booking


class TruckSaathiApp:
    """
    Application composition root.

    Responsible for constructing and wiring together all
    application dependencies.
    """

    def __init__(self) -> None:
        self.session_store = SQLiteSessionStore(
            settings.database_path,
        )

        self.booking_repository = (
            SQLiteBookingRepository(
                settings.database_path,
            )
        )

        self.dashboard_repository = (
            SQLiteDashboardRepository(
                settings.database_path,
            )
        )

        self.manager = ConversationManager(
            store=self.session_store,
            booking_repository=self.booking_repository,
            dashboard_repository=self.dashboard_repository,
            merge_engine=MergeEngine(),
            stt=transcribe,
            extractor=extract_booking,
            validator=validate_booking,
            followup_generator=generate_followup,
            followup_tts=synthesize_followup,
            confirmation_tts=synthesize_confirmation,
        )

    def close(self) -> None:
        """
        Gracefully close application resources.
        """

        self.session_store.close()

        self.booking_repository.close()

        self.dashboard_repository.close()