import pytest

from src.supervisor.session_repository import SessionRepository
from src.supervisor.session_state import SessionState


def build_repository():
    return SessionRepository()


def build_session(session_id="session-1"):
    return SessionState(
        session_id=session_id,
    )


def test_repository_starts_empty():
    repository = build_repository()

    assert repository.count() == 0
    assert repository.list_sessions() == []


def test_repository_saves_session():
    repository = build_repository()
    session = build_session()

    result = repository.save(session)

    assert result is session
    assert repository.count() == 1


def test_repository_gets_session():
    repository = build_repository()
    session = build_session()

    repository.save(session)

    result = repository.get("session-1")

    assert result is session


def test_repository_returns_none_for_missing_session():
    repository = build_repository()

    assert repository.get("missing") is None


def test_repository_checks_session_existence():
    repository = build_repository()
    session = build_session()

    assert repository.exists("session-1") is False

    repository.save(session)

    assert repository.exists("session-1") is True


def test_repository_deletes_session():
    repository = build_repository()
    repository.save(build_session())

    assert repository.delete("session-1") is True
    assert repository.exists("session-1") is False
    assert repository.count() == 0


def test_repository_delete_missing_session_returns_false():
    repository = build_repository()

    assert repository.delete("missing") is False


def test_repository_lists_sessions():
    repository = build_repository()

    first = build_session("session-1")
    second = build_session("session-2")

    repository.save(first)
    repository.save(second)

    assert repository.list_sessions() == [first, second]


def test_repository_replaces_session_with_same_id():
    repository = build_repository()

    first = build_session("session-1")
    second = build_session("session-1")

    first.pause()
    second.close()

    repository.save(first)
    repository.save(second)

    assert repository.count() == 1
    assert repository.get("session-1") is second
    assert repository.get("session-1").status == "closed"


def test_repository_clear_removes_all_sessions():
    repository = build_repository()

    repository.save(build_session("session-1"))
    repository.save(build_session("session-2"))

    repository.clear()

    assert repository.count() == 0
    assert repository.list_sessions() == []


def test_repository_rejects_invalid_session():
    repository = build_repository()

    with pytest.raises(TypeError):
        repository.save("invalid-session")


def test_repository_rejects_empty_session_id():
    repository = build_repository()

    session = build_session("")

    with pytest.raises(ValueError):
        repository.save(session)


def test_repository_normalizes_session_id_on_get():
    repository = build_repository()
    session = build_session("session-1")

    repository.save(session)

    assert repository.get("  session-1  ") is session


def test_repository_normalizes_session_id_on_delete():
    repository = build_repository()
    session = build_session("session-1")

    repository.save(session)

    assert repository.delete("  session-1  ") is True
    assert repository.exists("session-1") is False
