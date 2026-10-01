import pytest

from src.supervisor.session_state import SessionState


def build_session():
    return SessionState(
        session_id="session-1",
    )


def test_session_starts_active():
    session = build_session()

    assert session.session_id == "session-1"
    assert session.status == "active"
    assert session.task_ids == []
    assert session.metadata == {}


def test_session_adds_task():
    session = build_session()

    session.add_task("task-1")

    assert session.task_ids == ["task-1"]


def test_session_normalizes_task_id():
    session = build_session()

    session.add_task("  task-1  ")

    assert session.task_ids == ["task-1"]


def test_session_does_not_duplicate_task():
    session = build_session()

    session.add_task("task-1")
    session.add_task("task-1")

    assert session.task_ids == ["task-1"]


def test_session_removes_task():
    session = build_session()

    session.add_task("task-1")

    assert session.remove_task("task-1") is True
    assert session.task_ids == []


def test_session_remove_missing_task_returns_false():
    session = build_session()

    assert session.remove_task("missing") is False


def test_session_rejects_empty_task_id():
    session = build_session()

    with pytest.raises(ValueError):
        session.add_task("")


def test_session_can_be_paused():
    session = build_session()

    session.pause()

    assert session.status == "paused"


def test_session_can_be_activated():
    session = build_session()

    session.pause()
    session.activate()

    assert session.status == "active"


def test_session_can_be_closed():
    session = build_session()

    session.close()

    assert session.status == "closed"


def test_session_sets_metadata():
    session = build_session()

    session.set_metadata("source", "telegram")

    assert session.metadata["source"] == "telegram"


def test_session_rejects_empty_metadata_key():
    session = build_session()

    with pytest.raises(ValueError):
        session.set_metadata("", "value")


def test_session_to_dict():
    session = build_session()

    session.add_task("task-1")
    session.set_metadata("source", "telegram")
    session.pause()

    data = session.to_dict()

    assert data == {
        "session_id": "session-1",
        "status": "paused",
        "task_ids": ["task-1"],
        "metadata": {
            "source": "telegram",
        },
}
