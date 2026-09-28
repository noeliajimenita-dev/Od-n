import pytest

from src.telegram.connection_manager import TelegramConnectionManager
from src.telegram.connection_state import TelegramConnectionState


def test_register_bot():
    manager = TelegramConnectionManager()

    manager.register_bot("supervisor")

    assert (
        manager.get_state("supervisor")
        == TelegramConnectionState.DISCONNECTED
    )


def test_connection_transition():
    manager = TelegramConnectionManager()

    manager.register_bot("worker_1")

    manager.transition(
        "worker_1",
        TelegramConnectionState.CONNECTING,
    )

    assert (
        manager.get_state("worker_1")
        == TelegramConnectionState.CONNECTING
    )


def test_invalid_transition_raises_error():
    manager = TelegramConnectionManager()

    manager.register_bot("worker_2")

    with pytest.raises(ValueError):
        manager.transition(
            "worker_2",
            TelegramConnectionState.CONNECTED,
        )


def test_unknown_bot_raises_error():
    manager = TelegramConnectionManager()

    with pytest.raises(KeyError):
        manager.get_state("unknown_bot")
