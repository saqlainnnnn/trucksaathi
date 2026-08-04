from __future__ import annotations

from abc import ABC, abstractmethod

from conversation.session import ConversationSession


class SessionStore(ABC):

    @abstractmethod
    def get(self, user_id: str) -> ConversationSession | None:
        raise NotImplementedError

    @abstractmethod
    def save(self, session: ConversationSession) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: str) -> None:
        raise NotImplementedError

def save(self, session: ConversationSession) -> None:
    self._sessions[session.user_id] = session

    print(f"\n[MemorySessionStore] SAVE user_id={session.user_id}")
    print(f"  -> Session ID: {session.session_id}")
    print(f"  -> Turns: {len(session.turns)}")
    print(f"  -> Status: {session.status}")

    print("  -> Current booking:")

    for field_name in session.booking.model_fields:
        field = getattr(session.booking, field_name)
        print(f"     {field_name}: {field.value}")

    print(f"\n  -> Active sessions: {len(self._sessions)}")


def delete(self, user_id: str) -> None:
    self._sessions.pop(user_id, None)

    print(f"\n[MemorySessionStore] DELETE user_id={user_id}")
    print(f"  -> Active sessions: {len(self._sessions)}")
    @abstractmethod
    def save(self, session: ConversationSession) -> None:
        """
        Persist a conversation session.

        Implementations should insert new sessions and update existing
        ones transparently.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: str) -> None:
        """
        Delete the active session for a user.

        Safe to call even if no session exists.
        """
        raise NotImplementedError


class MemorySessionStore(SessionStore):
    """
    Simple in-memory implementation of SessionStore.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, ConversationSession] = {}

    def get(self, user_id: str) -> ConversationSession | None:
        session = self._sessions.get(user_id)

        print(f"\n[MemorySessionStore] GET {user_id}")

        if session is None:
            print(" -> No session found.")
        else:
            print(f" -> Loaded {session.session_id}")
            print(f" -> Turns: {len(session.turns)}")

        return session

    def save(self, session: ConversationSession) -> None:
        self._sessions[session.user_id] = session

        print(f"\n[MemorySessionStore] SAVE {session.user_id}")
        print(f" -> Turns: {len(session.turns)}")

        print(session.booking.model_dump_json(indent=2))

    def delete(self, user_id: str) -> None:
        self._sessions.pop(user_id, None)

        print(f"\n[MemorySessionStore] DELETE {user_id}")