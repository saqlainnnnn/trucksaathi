from __future__ import annotations

from collections.abc import Callable
from datetime import timedelta
from pathlib import Path

from conversation.merge import MergeEngine
from conversation.session import (
    ConversationResponse,
    ConversationSession,
    ConversationTurn,
    utc_now,
)
from conversation.store import SessionStore
from schemas import (
    BookingExtraction,
    ExtractionResult,
    TranscriptionResult,
    ValidationResult,
)

from booking.repository import BookingRepository

SESSION_TIMEOUT = timedelta(minutes=30)

STTFunction = Callable[[str | Path], TranscriptionResult]
ExtractorFunction = Callable[[str], ExtractionResult]
ValidatorFunction = Callable[[BookingExtraction], ValidationResult]
FollowupFunction = Callable[[BookingExtraction, ValidationResult], str]
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
        merge_engine: MergeEngine,
        stt: STTFunction,
        extractor: ExtractorFunction,
        validator: ValidatorFunction,
        followup_generator: FollowupFunction,
        followup_tts: FollowupTTSFunction,
        confirmation_tts: ConfirmationTTSFunction,
    ) -> None:
        """
        Initialize the conversation manager with all required dependencies.
        """

        self._store = store

        self._booking_repository = booking_repository

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
        session = self._load_session(user_id)

        transcription = self._stt(audio_path)

        extraction = self._extractor(
            transcription.transcript,
        )

        merged_booking = self._merge.merge(
            session.booking,
            extraction.booking,
        )

        print("\n[MergeEngine] Booking after merge:")
        print(merged_booking.model_dump_json(indent=2))

        session.update_booking(merged_booking)

        validation = self._validator(
            session.booking,
        )

        if validation.is_complete:
            reply_text = (
                "Aapki truck booking safalta se confirm ho gayi hai. Dhanyavaad."
            )

            audio = self._confirmation_tts()

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

            self._store.delete(user_id)

            return ConversationResponse(
                transcript=transcription.transcript,
                reply_text=reply_text,
                reply_audio_path=audio,
                completed=True,
                booking=session.booking,
            )

        reply_text = self._followup(
            session.booking,
            validation,
        )

        audio = self._followup_tts(reply_text)

        session.add_turn(
            ConversationTurn(
                user_transcript=transcription.transcript,
                assistant_reply=reply_text,
                extraction=extraction.booking,
            )
        )

        self._store.save(session)

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
        session = self._store.get(user_id)

        if session is None:
            session = ConversationSession(user_id=user_id)
            self._store.save(session)
            return session

        if utc_now() - session.updated_at > SESSION_TIMEOUT:
            self._store.delete(user_id)

            session = ConversationSession(user_id=user_id)
            self._store.save(session)

        return session