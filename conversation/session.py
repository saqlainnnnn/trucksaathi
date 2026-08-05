from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from uuid import UUID, uuid4

from schemas import BookingExtraction


def utc_now() -> datetime:
    """
    Return the current UTC timestamp.
    """
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
    """

    user_transcript: str

    assistant_reply: str

    extraction: BookingExtraction

    timestamp: datetime = field(default_factory=utc_now)

    def to_dict(self) -> dict:
        """
        Serialize the conversation turn.
        """

        return {
            "user_transcript": self.user_transcript,
            "assistant_reply": self.assistant_reply,
            "extraction": self.extraction.model_dump(),
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "ConversationTurn":
        """
        Deserialize a conversation turn.
        """

        return cls(
            user_transcript=data["user_transcript"],
            assistant_reply=data["assistant_reply"],
            extraction=BookingExtraction.model_validate(
                data["extraction"]
            ),
            timestamp=datetime.fromisoformat(
                data["timestamp"]
            ),
        )


@dataclass(slots=True)
class ConversationSession:
    """
    Represents the complete state of an ongoing booking conversation.
    """

    user_id: str

    booking: BookingExtraction = field(
        default_factory=BookingExtraction,
    )

    session_id: UUID = field(
        default_factory=uuid4,
    )

    status: ConversationStatus = (
        ConversationStatus.IN_PROGRESS
    )

    turns: list[ConversationTurn] = field(
        default_factory=list,
    )

    created_at: datetime = field(
        default_factory=utc_now,
    )

    updated_at: datetime = field(
        default_factory=utc_now,
    )

    def add_turn(
        self,
        turn: ConversationTurn,
    ) -> None:
        """
        Append a conversation turn.
        """

        self.turns.append(turn)
        self.touch()

    def update_booking(
        self,
        booking: BookingExtraction,
    ) -> None:
        """
        Replace the current booking snapshot.
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
        Update the last-modified timestamp.
        """

        self.updated_at = utc_now()

    def to_dict(self) -> dict:
        """
        Serialize the conversation session.
        """

        return {
            "session_id": str(self.session_id),
            "user_id": self.user_id,
            "status": self.status.value,
            "booking": self.booking.model_dump(),
            "turns": [
                turn.to_dict()
                for turn in self.turns
            ],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "ConversationSession":
        """
        Deserialize a conversation session.
        """

        return cls(
            session_id=UUID(
                data["session_id"]
            ),
            user_id=data["user_id"],
            status=ConversationStatus(
                data["status"]
            ),
            booking=BookingExtraction.model_validate(
                data["booking"]
            ),
            turns=[
                ConversationTurn.from_dict(turn)
                for turn in data["turns"]
            ],
            created_at=datetime.fromisoformat(
                data["created_at"]
            ),
            updated_at=datetime.fromisoformat(
                data["updated_at"]
            ),
        )


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