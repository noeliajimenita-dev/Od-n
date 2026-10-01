import pytest

from src.supervisor.session_recovery_service import SessionRecoveryService
from src.supervisor.session_repository import SessionRepository
from src.supervisor.session_snapshot import SessionSnapshot
from src.supervisor.session_state import SessionState


def build_service():
    return SessionRecoveryService(SessionRepository())


def build_snapshot(
    session_id="session-1",
    status="paused",
):
    return SessionSnapshot(
        session_id=session_id,
        status=status,
        task_ids=["task-1", "task-2"],
        metadata={
            "source": "backup",
        },
    )


def test_service_requires_repository():
    with pytest.raises(ValueError):
        SessionRecoveryService(None)


def test_service_recovers_session_from_snapshot():
    service = build_service()
    snapshot = build_snapshot()

    session = service.recover(snapshot)

    assert isinstance(session, SessionState)
    assert session.session_id == "session-1"
    assert session.status == "paused"
    assert session.task_ids == ["task-1", "task-2"]


def test_service_stores_recovered_session():
    service = build_service()

    service.recover(build_snapshot())

    recovered = service.get_recovered("session-1")

    assert recovered is not None
    assert recovered.session_id == "session-1"


def test_service_recovers_from_dictionary():
    service = build_service()

    data = {
        "session_id": "session-2",
        "status": "active",
        "task_ids": ["task-3"],
        "metadata": {
            "source": "telegram",
        },
    }

    session = service.recover_from_dict(data)

    assert isinstance(session, SessionState)
    assert session.session_id == "session-2"
    assert session.status == "active"
    assert session.task_ids == ["task-3"]
    assert session.metadata["source"] == "telegram"


def test_service_recovers_multiple_sessions():
    service = build_service()

    snapshots = [
        build_snapshot("session-1", "active"),
        build_snapshot("session-2", "paused"),
        build_snapshot("session-3", "closed"),
    ]

    sessions = service.recover_all(snapshots)

    assert len(sessions) == 3
    assert [session.session_id for session in sessions] == [
        "session-1",
        "session-2",
        "session-3",
    ]


def test_service_counts_recovered_sessions():
    service = build_service()

    service.recover(build_snapshot("session-1"))
    service.recover(build_snapshot("session-2"))

    assert service.count_recovered() == 2


def test_service_rejects_invalid_snapshot():
    service = build_service()

    with pytest.raises(TypeError):
        service.recover("invalid-snapshot")


def test_service_rejects_missing_snapshots():
    service = build_service()

    with pytest.raises(ValueError):
        service.recover_all(None)


def test_service_preserves_metadata():
    service = build_service()

    session = service.recover(build_snapshot())

    assert session.metadata == {
        "source": "backup",
    }


def test_service_replaces_existing_session_with_same_id():
    service = build_service()

    service.recover(
        build_snapshot(
            "session-1",
            "paused",
        )
    )

    service.recover(
        build_snapshot(
            "session-1",
            "active",
        )
    )

    recovered = service.get_recovered("session-1")

    assert recovered.status == "active"
    assert service.count_recovered() == 1


def test_service_missing_session_returns_none():
    service = build_service()

    assert service.get_recovered("missing") is None
