from pathlib import Path

from conversation.manager import ConversationManager
from conversation.merge import MergeEngine
from conversation.store import MemorySessionStore
from schemas import (
    BookingExtraction,
    BookingField,
    ExtractionResult,
    TranscriptionResult,
    ValidationResult,
)


def fake_stt(path):
    return TranscriptionResult(
        transcript="Mumbai to Pune",
    )


def fake_extractor(text):
    booking = BookingExtraction(
        pickup=BookingField(value="Mumbai"),
        destination=BookingField(value="Pune"),
    )

    return ExtractionResult(
        transcript=text,
        booking=booking,
        model="fake",
    )


def fake_validator(booking):
    return ValidationResult(
        is_complete=False,
        missing_fields=["truck_type"],
    )


def fake_followup(booking, validation):
    return "Truck type?"


def fake_tts(text):
    return Path("output/test.wav")


def test_conversation_manager_followup():
    manager = ConversationManager(
        store=MemorySessionStore(),
        merge_engine=MergeEngine(),
        stt=fake_stt,
        extractor=fake_extractor,
        validator=fake_validator,
        followup_generator=fake_followup,
        followup_tts=fake_tts,
        confirmation_tts=lambda: Path("output/confirmation.wav"),
    )

    response = manager.process(
        user_id="demo-user",
        audio_path="dummy.wav",
    )

    assert response.completed is False
    assert response.reply_text == "Truck type?"
    assert response.booking.pickup.value == "Mumbai"
    assert response.booking.destination.value == "Pune"