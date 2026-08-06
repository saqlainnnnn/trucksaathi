from __future__ import annotations

from collections.abc import Callable
from datetime import timedelta
from pathlib import Path
from time import perf_counter

from booking.repository import BookingRepository
from conversation.merge import MergeEngine
from conversation.session import (
    ConversationResponse,
    ConversationSession,
    ConversationTurn,
    utc_now,
)
from conversation.store import SessionStore
from dashboard.repository import DashboardRepository
from schemas import (
    BookingExtraction,
    ExtractionResult,
    TranscriptionResult,
    ValidationResult,
)

from dashboard.models import DashboardEvent

SESSION_TIMEOUT = timedelta(minutes=30)

STTFunction = Callable[[str | Path], TranscriptionResult]
ExtractorFunction = Callable[[str], ExtractionResult]
ValidatorFunction = Callable[[BookingExtraction], ValidationResult]
FollowupFunction = Callable[
    [BookingExtraction, ValidationResult],
    str,
]
FollowupTTSFunction = Callable[[str], Path]
ConfirmationTTSFunction = Callable[[], Path]


class ConversationManager:
    """
    Coordinates the TruckSaathi conversation workflow.
    """

    def __init__(
        self,
        store: SessionStore,
        booking_repository: BookingRepository,
        dashboard_repository: DashboardRepository,
        merge_engine: MergeEngine,
        stt: STTFunction,
        extractor: ExtractorFunction,
        validator: ValidatorFunction,
        followup_generator: FollowupFunction,
        followup_tts: FollowupTTSFunction,
        confirmation_tts: ConfirmationTTSFunction,
    ) -> None:

        self._store = store
        self._booking_repository = booking_repository
        self._dashboard = dashboard_repository

        self._merge = merge_engine
        self._stt = stt
        self._extractor = extractor
        self._validator = validator
        self._followup = followup_generator
        self._followup_tts = followup_tts
        self._confirmation_tts = confirmation_tts

    def process(
        self,
        user_id: str,
        audio_path: str | Path,
    ) -> ConversationResponse:

        session = self._load_session(
            user_id,
        )

        #
        # STT
        #

        self._dashboard.stage_started(
            "stt",
        )

        start = perf_counter()

        transcription = self._stt(
            audio_path,
        )

        self._dashboard.save(
            DashboardEvent(
                event_type="conversation",
                payload={
                    "role": "user",
                    "text": transcription.transcript,
                },
            )
        )

        self._dashboard.stage_finished(
            "stt",
            (perf_counter() - start)
            * 1000,
        )

        self._dashboard.log(
            "Speech transcription completed.",
        )

        #
        # Extraction
        #

        self._dashboard.stage_started(
            "extract",
        )

        start = perf_counter()

        extraction = self._extractor(
            transcription.transcript,
        )

        self._dashboard.stage_finished(
            "extract",
            (perf_counter() - start)
            * 1000,
        )

        self._dashboard.log(
            "Booking extracted.",
        )

        #
        # Merge
        #

        self._dashboard.stage_started(
            "merge",
        )

        start = perf_counter()

        merged_booking = self._merge.merge(
            session.booking,
            extraction.booking,
        )

        self._dashboard.stage_finished(
            "merge",
            (perf_counter() - start)
            * 1000,
        )

        self._dashboard.log(
            "Booking merged.",
        )

        print("\n[MergeEngine] Booking after merge:")
        print(
            merged_booking.model_dump_json(
                indent=2,
            )
        )

        session.update_booking(
            merged_booking,
        )

        self._dashboard.save(
            DashboardEvent(
                event_type="booking_updated",
                payload=merged_booking.model_dump(),
            )
        )

        #
        # Validation
        #

        self._dashboard.stage_started(
            "validation",
        )

        start = perf_counter()

        validation = self._validator(
            session.booking,
        )

        self._dashboard.stage_finished(
            "validation",
            (perf_counter() - start)
            * 1000,
        )

        self._dashboard.log(
            "Booking validated.",
        )

        if validation.is_complete:

            self._dashboard.stage_started(
                "tts",
            )

            start = perf_counter()

            reply_text = (
                "Aapki truck booking safalta se confirm ho gayi hai. Dhanyavaad."
            )

            audio = self._confirmation_tts()

            self._dashboard.stage_finished(
                "tts",
                (perf_counter() - start) * 1000,
            )

            self._dashboard.log(
                "Confirmation synthesized.",
            )

            session.mark_completed()

            session.add_turn(
                ConversationTurn(
                    user_transcript=transcription.transcript,
                    assistant_reply=reply_text,
                    extraction=extraction.booking,
                )
            )

            self._booking_repository.save(
                session.booking,
            )

            self._store.delete(
                user_id,
            )

            return ConversationResponse(
                transcript=transcription.transcript,
                reply_text=reply_text,
                reply_audio_path=audio,
                completed=True,
                booking=session.booking,
            )
        #
        # Follow-up
        #

        self._dashboard.stage_started(
            "followup",
        )

        start = perf_counter()

        reply_text = self._followup(
            session.booking,
            validation,
        )

        self._dashboard.save(
            DashboardEvent(
                event_type="conversation",
                payload={
                    "role": "assistant",
                    "text": reply_text,
                },
            )
        )

        self._dashboard.stage_finished(
            "followup",
            (perf_counter() - start)
            * 1000,
        )

        self._dashboard.log(
            "Follow-up generated.",
        )

        #
        # Follow-up TTS
        #

        self._dashboard.stage_started(
            "tts",
        )

        start = perf_counter()

        audio = self._followup_tts(
            reply_text,
        )

        self._dashboard.stage_finished(
            "tts",
            (perf_counter() - start)
            * 1000,
        )

        self._dashboard.log(
            "Speech synthesized.",
        )

        session.add_turn(
            ConversationTurn(
                user_transcript=transcription.transcript,
                assistant_reply=reply_text,
                extraction=extraction.booking,
            )
        )

        self._store.save(
            session,
        )

        return ConversationResponse(
            transcript=transcription.transcript,
            reply_text=reply_text,
            reply_audio_path=audio,
            completed=False,
            booking=session.booking,
        )

    def _load_session(
        self,
        user_id: str,
    ) -> ConversationSession:

        session = self._store.get(
            user_id,
        )

        if session is None:

            session = ConversationSession(
                user_id=user_id,
            )

            self._store.save(
                session,
            )

            return session

        if (
            utc_now()
            - session.updated_at
            > SESSION_TIMEOUT
        ):

            self._store.delete(
                user_id,
            )

            session = ConversationSession(
                user_id=user_id,
            )

            self._store.save(
                session,
            )

        return session