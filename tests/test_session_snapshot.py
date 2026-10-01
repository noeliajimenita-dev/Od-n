import pytest

from src.supervisor.session_snapshot import SessionSnapshot
from src.supervisor.session_state import SessionState


def build_session():
    session = SessionState(
        session_id="session-1",
        status="paused",
        task_ids=["task-1", "task-2"],
        metadata={
            "source": "telegram",
            "user": "supervisor",
        },
    )
    return session


def test_snapshot_is_created_from_session():
    session = build_session()

    snapshot = SessionSnapshot.from_session(session)

    assert snapshot.session_id == "session-1"
    assert snapshot.status == "paused"
    assert snapshot.task_ids == ["task-1", "task-2"]
    assert snapshot.metadata == {
        "source": "telegram",
        "user": "supervisor",
    }


def test_snapshot_to_dict():
    snapshot = SessionSnapshot.from_session(build_session())

    data = snapshot.to_dict()

    assert data == {
        "session_id": "session-1",
        "status": "paused",
        "task_ids": ["task-1", "task-2"],
        "metadata": {
            "source": "telegram",
            "user": "supervisor",
        },
    }


def test_snapshot_from_dict():
    data = {
        "session_id": "session-2",
        "status": "active",
        "task_ids": ["task-3"],
        "metadata": {
            "source": "restore",
        },
    }

    snapshot = SessionSnapshot.from_dict(data)

    assert snapshot.session_id == "session-2"
    assert snapshot.status == "active"
    assert snapshot.task_ids == ["task-3"]
    assert snapshot.metadata["source"] == "restore"


def test_snapshot_converts_back_to_session():
    original = build_session()

    snapshot = SessionSnapshot.from_session(original)
    restored = snapshot.to_session()

    assert isinstance(restored, SessionState)
    assert restored.session_id == original.session_id
    assert restored.status == original.status
    assert restored.task_ids == original.task_ids
    assert restored.metadata == original.metadata


def test_snapshot_preserves_lists_independently():
    session = build_session()

    snapshot = SessionSnapshot.from_session(session)
    snapshot.task_ids.append("task-3")

    assert "task-3" not in session.task_ids


def test_snapshot_preserves_metadata_independently():
    session = build_session()

    snapshot = SessionSnapshot.from_session(session)
    snapshot.metadata["new_value"] = True

    assert "new_value" not in session.metadata


def test_snapshot_rejects_invalid_session():
    with pytest.raises(TypeError):
        SessionSnapshot.from_session("invalid-session")


def test_snapshot_rejects_invalid_data():
    with pytest.raises(TypeError):
        SessionSnapshot.from_dict("invalid-data")


def test_snapshot_rejects_empty_session_id():
    data = {
        "session_id": "",
        "status": "active",
    }

    with pytest.raises(ValueError):
        SessionSnapshot.from_dict(data)


def test_snapshot_normalizes_session_id():
    data = {
        "session_id": "  session-1  ",
        "status": "active",
    }

    snapshot = SessionSnapshot.from_dict(data)

    assert snapshot.session_id == "session-1"


def test_snapshot_round_trip_preserves_state():
    original = build_session()

    snapshot = SessionSnapshot.from_session(original)
    data = snapshot.to_dict()
    restored_snapshot = SessionSnapshot.from_dict(data)
    restored = restored_snapshot.to_session()

    assert restored.session_id == original.session_id
    assert restored.status == original.status
    assert restored.task_ids == original.task_ids
    assert restored.metadata == original.metadata
