import pytest

from src.telegram.connection_registry import TelegramConnectionRegistry


def test_register_session():
    registry = TelegramConnectionRegistry()

    session = registry.register("worker_1")

    assert session.bot_name == "worker_1"
    assert registry.count() == 1


def test_get_registered_session():
    registry = TelegramConnectionRegistry()

    registry.register("worker_1")

    session = registry.get("worker_1")

    assert session.bot_name == "worker_1"


def test_duplicate_registration_is_blocked():
    registry = TelegramConnectionRegistry()

    registry.register("worker_1")

    with pytest.raises(ValueError):
        registry.register("worker_1")


def test_get_all_sessions():
    registry = TelegramConnectionRegistry()

    registry.register("supervisor")
    registry.register("worker_1")

    sessions = registry.get_all()

    assert len(sessions) == 2
    assert "supervisor" in sessions
    assert "worker_1" in sessions


def test_remove_session():
    registry = TelegramConnectionRegistry()

    registry.register("worker_1")
    registry.remove("worker_1")

    assert registry.count() == 0

    with pytest.raises(KeyError):
        registry.get("worker_1")


def test_invalid_bot_name_is_blocked():
    registry = TelegramConnectionRegistry()

    with pytest.raises(ValueError):
        registry.register("")
