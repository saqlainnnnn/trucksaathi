from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from conversation.session import ConversationSession
from conversation.store import SessionStore


class SQLiteSessionStore(SessionStore):
    """
    SQLite-backed implementation of SessionStore.

    Stores the complete ConversationSession as JSON.
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
        """
        Create database tables if they do not exist.
        """

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS conversation_sessions (

                user_id TEXT PRIMARY KEY,

                payload TEXT NOT NULL

            );
            """
        )

        self._connection.commit()

    def get(
        self,
        user_id: str,
    ) -> ConversationSession | None:
        """
        Load the active session for a user.
        """

        cursor = self._connection.execute(
            """
            SELECT payload
            FROM conversation_sessions
            WHERE user_id = ?
            """,
            (user_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        payload = json.loads(
            row["payload"],
        )

        return ConversationSession.from_dict(
            payload,
        )

    def save(
        self,
        session: ConversationSession,
    ) -> None:
        """
        Insert or update a session.
        """

        payload = json.dumps(
            session.to_dict(),
            ensure_ascii=False,
        )

        self._connection.execute(
            """
            INSERT INTO conversation_sessions (
                user_id,
                payload
            )
            VALUES (?, ?)

            ON CONFLICT(user_id)

            DO UPDATE SET

                payload = excluded.payload
            """,
            (
                session.user_id,
                payload,
            ),
        )

        self._connection.commit()

    def delete(
        self,
        user_id: str,
    ) -> None:
        """
        Delete a user's active session.
        """

        self._connection.execute(
            """
            DELETE FROM conversation_sessions
            WHERE user_id = ?
            """,
            (user_id,),
        )

        self._connection.commit()

    def close(self) -> None:
        """
        Close the SQLite connection.
        """

        self._connection.close()