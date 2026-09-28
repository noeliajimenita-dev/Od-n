from src.telegram.connection_state import (
    TelegramConnectionState,
    can_transition,
)


def test_disconnected_can_connect():
    assert can_transition(
        TelegramConnectionState.DISCONNECTED,
        TelegramConnectionState.CONNECTING,
    )


def test_connecting_can_become_connected():
    assert can_transition(
        TelegramConnectionState.CONNECTING,
        TelegramConnectionState.CONNECTED,
    )


def test_connected_can_reconnect():
    assert can_transition(
        TelegramConnectionState.CONNECTED,
        TelegramConnectionState.RECONNECTING,
    )


def test_stopped_cannot_transition():
    assert not can_transition(
        TelegramConnectionState.STOPPED,
        TelegramConnectionState.CONNECTING,
    )


def test_disconnected_cannot_become_connected_directly():
    assert not can_transition(
        TelegramConnectionState.DISCONNECTED,
        TelegramConnectionState.CONNECTED,
    )
