from src.telegram.connection_registry import TelegramConnectionRegistry
from src.telegram.connection_recovery_status import (
    get_connection_recovery_status,
)


def test_recovery_status_empty_registry():
    registry = TelegramConnectionRegistry()

    status = get_connection_recovery_status(registry)

    assert status["total_bots"] == 0
    assert status["recovered_bots"] == 0
    assert status["bots_needing_recovery"] == 0
    assert status["recovered_bot_names"] == []
    assert status["bots_needing_recovery_names"] == []


def test_recovery_status_with_disconnected_bots():
    registry = TelegramConnectionRegistry()

    registry.register("supervisor")
    registry.register("worker_1")

    status = get_connection_recovery_status(registry)

    assert status["total_bots"] == 2
    assert status["recovered_bots"] == 0
    assert status["bots_needing_recovery"] == 2
    assert status["recovered_bot_names"] == []
    assert set(status["bots_needing_recovery_names"]) == {
        "supervisor",
        "worker_1",
    }


def test_recovery_status_with_connected_bots():
    registry = TelegramConnectionRegistry()

    supervisor = registry.register("supervisor")
    worker_1 = registry.register("worker_1")
    registry.register("worker_2")

    supervisor.connect()
    worker_1.connect()

    status = get_connection_recovery_status(registry)

    assert status["total_bots"] == 3
    assert status["recovered_bots"] == 2
    assert status["bots_needing_recovery"] == 1

    assert set(status["recovered_bot_names"]) == {
        "supervisor",
        "worker_1",
    }

    assert status["bots_needing_recovery_names"] == ["worker_2"]
