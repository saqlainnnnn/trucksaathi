from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from schemas import BookingExtraction


def utc_now() -> datetime:
    """Return the current UTC timestamp."""

    return datetime.now(timezone.utc)


class ConversationStatus(str, Enum):
    """
    Current lifecycle state of a conversation.
    """

    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass(slots=True)
class ConversationTurn:
    """
    Represents a single interaction between the user and TruckSaathi.

    Each turn stores the user's transcript, the assistant's reply,
    and the structured booking information extracted from that
    transcript.
    """

    user_transcript: str

    assistant_reply: str

    extraction: BookingExtraction

    timestamp: datetime = field(default_factory=utc_now)


@dataclass(slots=True)
class ConversationSession:
    """
    Represents the complete state of an ongoing booking conversation.

    A session is transport-independent and contains only domain state.
    """

    user_id: str

    booking: BookingExtraction = field(default_factory=BookingExtraction)

    session_id: UUID = field(default_factory=uuid4)

    status: ConversationStatus = ConversationStatus.IN_PROGRESS

    turns: list[ConversationTurn] = field(default_factory=list)

    created_at: datetime = field(default_factory=utc_now)

    updated_at: datetime = field(default_factory=utc_now)

    def add_turn(self, turn: ConversationTurn) -> None:
        """
        Append a conversation turn and update the session timestamp.
        """

        self.turns.append(turn)
        self.touch()

    def update_booking(self, booking: BookingExtraction) -> None:
        """
        Replace the current booking snapshot.

        Merge logic is intentionally handled elsewhere by MergeEngine.
        """

        self.booking = booking
        self.touch()

    def mark_completed(self) -> None:
        """
        Mark the conversation as completed.
        """

        self.status = ConversationStatus.COMPLETED
        self.touch()

    def touch(self) -> None:
        """
        Update the session's last-modified timestamp.
        """

        self.updated_at = utc_now()

@dataclass(slots=True)
class ConversationResponse:
    """
    Output returned by ConversationManager.
    """

    transcript: str

    reply_text: str

    reply_audio_path: Path

    completed: bool

    booking: BookingExtraction