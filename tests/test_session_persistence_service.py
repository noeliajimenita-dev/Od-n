import pytest

from src.supervisor.session_persistence_service import (
    SessionPersistenceService,
)
from src.supervisor.session_repository import SessionRepository
from src.supervisor.session_state import SessionState


def build_service():
    return SessionPersistenceService(SessionRepository())


def build_session(session_id="session-1"):
    return SessionState(
        session_id=session_id,
    )


def test_service_requires_repository():
    with pytest.raises(ValueError):
        SessionPersistenceService(None)


def test_service_saves_session():
    service = build_service()
    session = build_session()

    result = service.save(session)

    assert result is session
    assert service.count() == 1


def test_service_gets_session():
    service = build_service()
    session = build_session()

    service.save(session)

    assert service.get("session-1") is session


def test_service_checks_session_existence():
    service = build_service()
    session = build_session()

    assert service.exists("session-1") is False

    service.save(session)

    assert service.exists("session-1") is True


def test_service_updates_existing_session():
    service = build_service()

    original = build_session()
    service.save(original)

    updated = build_session()
    updated.pause()

    result = service.update(updated)

    assert result is updated
    assert service.get("session-1").status == "paused"
    assert service.count() == 1


def test_service_rejects_update_for_missing_session():
    service = build_service()

    with pytest.raises(ValueError):
        service.update(build_session("missing"))


def test_service_deletes_session():
    service = build_service()
    service.save(build_session())

    assert service.delete("session-1") is True
    assert service.exists("session-1") is False


def test_service_lists_sessions():
    service = build_service()

    first = build_session("session-1")
    second = build_session("session-2")

    service.save(first)
    service.save(second)

    assert service.list_sessions() == [first, second]


def test_service_counts_sessions():
    service = build_service()

    service.save(build_session("session-1"))
    service.save(build_session("session-2"))

    assert service.count() == 2


def test_service_clears_sessions():
    service = build_service()

    service.save(build_session("session-1"))
    service.save(build_session("session-2"))

    service.clear()

    assert service.count() == 0
    assert service.list_sessions() == []


def test_service_rejects_invalid_session():
    service = build_service()

    with pytest.raises(TypeError):
        service.save("invalid-session")


def test_service_rejects_invalid_session_on_update():
    service = build_service()

    with pytest.raises(TypeError):
        service.update("invalid-session")
