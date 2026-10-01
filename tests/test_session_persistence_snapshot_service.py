import pytest

from src.supervisor.session_persistence_service import SessionPersistenceService
from src.supervisor.session_persistence_snapshot_service import (
    SessionPersistenceSnapshotService,
)
from src.supervisor.session_repository import SessionRepository
from src.supervisor.session_snapshot import SessionSnapshot
from src.supervisor.session_state import SessionState


def build_service():
    repository = SessionRepository()
    persistence = SessionPersistenceService(repository)
    return SessionPersistenceSnapshotService(persistence)


def build_session(session_id="session-1", status="active"):
    return SessionState(
        session_id=session_id,
        status=status,
        task_ids=["task-1", "task-2"],
        metadata={"source": "supervisor"},
    )


def test_service_requires_persistence_service():
    with pytest.raises(ValueError):
        SessionPersistenceSnapshotService(None)


def test_service_creates_snapshot_from_session():
    service = build_service()
    session = build_session()

    snapshot = service.create_snapshot(session)

    assert isinstance(snapshot, SessionSnapshot)
    assert snapshot.session_id == "session-1"
    assert snapshot.status == "active"
    assert snapshot.task_ids == ["task-1", "task-2"]


def test_service_rejects_invalid_session_when_creating_snapshot():
    service = build_service()

    with pytest.raises(TypeError):
        service.create_snapshot("invalid-session")


def test_service_saves_snapshot():
    service = build_service()
    snapshot = service.create_snapshot(build_session())

    saved = service.save_snapshot(snapshot)

    assert saved is snapshot
    assert service.count_snapshots() == 1


def test_service_rejects_invalid_snapshot():
    service = build_service()

    with pytest.raises(TypeError):
        service.save_snapshot("invalid-snapshot")


def test_service_saves_session_as_snapshot():
    service = build_service()
    session = build_session("session-2", "paused")

    snapshot = service.save_session_snapshot(session)

    assert isinstance(snapshot, SessionSnapshot)
    assert snapshot.session_id == "session-2"
    assert snapshot.status == "paused"
    assert service.count_snapshots() == 1


def test_service_gets_snapshot():
    service = build_service()
    session = build_session()
    service.save_session_snapshot(session)

    snapshot = service.get_snapshot("session-1")

    assert isinstance(snapshot, SessionSnapshot)
    assert snapshot.session_id == "session-1"
    assert snapshot.task_ids == ["task-1", "task-2"]


def test_service_returns_none_for_missing_snapshot():
    service = build_service()

    assert service.get_snapshot("missing") is None


def test_service_lists_snapshots():
    service = build_service()

    service.save_session_snapshot(build_session("session-1"))
    service.save_session_snapshot(build_session("session-2", "paused"))
    service.save_session_snapshot(build_session("session-3", "closed"))

    snapshots = service.list_snapshots()

    assert len(snapshots) == 3
    assert [snapshot.session_id for snapshot in snapshots] == [
        "session-1",
        "session-2",
        "session-3",
    ]


def test_service_counts_snapshots():
    service = build_service()

    service.save_session_snapshot(build_session("session-1"))
    service.save_session_snapshot(build_session("session-2"))

    assert service.count_snapshots() == 2


def test_service_preserves_metadata():
    service = build_service()
    session = build_session()

    snapshot = service.save_session_snapshot(session)

    assert snapshot.metadata == {"source": "supervisor"}


def test_service_replaces_snapshot_with_same_session_id():
    service = build_service()

    service.save_session_snapshot(build_session("session-1", "paused"))
    service.save_session_snapshot(build_session("session-1", "active"))

    snapshot = service.get_snapshot("session-1")

    assert snapshot.status == "active"
    assert service.count_snapshots() == 1
