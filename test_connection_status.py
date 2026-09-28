from src.telegram.connection_manager import TelegramConnectionManager
from src.telegram.connection_state import TelegramConnectionState
from src.telegram.connection_status import get_connection_status


def test_connection_status():
    manager = TelegramConnectionManager()

    manager.register_bot("supervisor")
    manager.register_bot("worker_1")
    manager.register_bot("worker_2")

    manager.transition(
        "supervisor",
        TelegramConnectionState.CONNECTING,
    )
    manager.transition(
        "supervisor",
        TelegramConnectionState.CONNECTED,
    )

    manager.transition(
        "worker_1",
        TelegramConnectionState.CONNECTING,
    )

    status = get_connection_status(manager)

    assert status["total_bots"] == 3
    assert status["connected_bots"] == 1
    assert status["states"]["CONNECTED"] == 1
    assert status["states"]["CONNECTING"] == 1
    assert status["states"]["DISCONNECTED"] == 1


def test_empty_connection_status():
    manager = TelegramConnectionManager()

    status = get_connection_status(manager)

    assert status["total_bots"] == 0
    assert status["connected_bots"] == 0
    assert status["error_bots"] == 0
    assert status["stopped_bots"] == 0
