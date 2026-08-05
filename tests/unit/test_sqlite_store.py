from conversation.session import ConversationSession
from conversation.sqlite_store import SQLiteSessionStore


def test_sqlite_session_store_roundtrip(tmp_path):
    """
    Sessions should survive a save/load/delete roundtrip.
    """

    database = tmp_path / "trucksaathi.db"

    store = SQLiteSessionStore(database)

    session = ConversationSession(
        user_id="demo-user",
    )

    #
    # Save
    #

    store.save(session)

    #
    # Load
    #

    loaded = store.get("demo-user")

    assert loaded is not None

    assert loaded.to_dict() == session.to_dict()

    #
    # Delete
    #

    store.delete("demo-user")

    assert store.get("demo-user") is None

    store.close()