from enum import Enum


class TelegramConnectionState(str, Enum):
    DISCONNECTED = "DISCONNECTED"
    CONNECTING = "CONNECTING"
    CONNECTED = "CONNECTED"
    RECONNECTING = "RECONNECTING"
    ERROR = "ERROR"
    STOPPED = "STOPPED"


VALID_CONNECTION_TRANSITIONS = {
    TelegramConnectionState.DISCONNECTED: {
        TelegramConnectionState.CONNECTING,
        TelegramConnectionState.STOPPED,
    },
    TelegramConnectionState.CONNECTING: {
        TelegramConnectionState.CONNECTED,
        TelegramConnectionState.ERROR,
        TelegramConnectionState.STOPPED,
    },
    TelegramConnectionState.CONNECTED: {
        TelegramConnectionState.RECONNECTING,
        TelegramConnectionState.DISCONNECTED,
        TelegramConnectionState.STOPPED,
    },
    TelegramConnectionState.RECONNECTING: {
        TelegramConnectionState.CONNECTED,
        TelegramConnectionState.ERROR,
        TelegramConnectionState.STOPPED,
    },
    TelegramConnectionState.ERROR: {
        TelegramConnectionState.CONNECTING,
        TelegramConnectionState.RECONNECTING,
        TelegramConnectionState.STOPPED,
    },
    TelegramConnectionState.STOPPED: set(),
}


def can_transition(
    current: TelegramConnectionState,
    target: TelegramConnectionState,
) -> bool:
    return target in VALID_CONNECTION_TRANSITIONS.get(current, set())
