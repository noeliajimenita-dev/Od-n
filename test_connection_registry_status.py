from src.telegram.connection_registry import TelegramConnectionRegistry
from src.telegram.connection_registry_status import (
    get_connection_registry_status,
)


def test_registry_status_empty():
    registry = TelegramConnectionRegistry()

    status = get_connection_registry_status(registry)

    assert status["total_sessions"] == 0
    assert status["connected_sessions"] == 0
    assert status["disconnected_sessions"] == 0
    assert status["connected_bots"] == []


def test_registry_status_with_disconnected_sessions():
    registry = TelegramConnectionRegistry()

    registry.register("supervisor")
    registry.register("worker_1")

    status = get_connection_registry_status(registry)

    assert status["total_sessions"] == 2
    assert status["connected_sessions"] == 0
    assert status["disconnected_sessions"] == 2
    assert status["connected_bots"] == []


def test_registry_status_with_connected_sessions():
    registry = TelegramConnectionRegistry()

    supervisor = registry.register("supervisor")
    worker_1 = registry.register("worker_1")

    supervisor.connect()

    status = get_connection_registry_status(registry)

    assert status["total_sessions"] == 2
    assert status["connected_sessions"] == 1
    assert status["disconnected_sessions"] == 1
    assert status["connected_bots"] == ["supervisor"]


def test_registry_status_with_multiple_connected_sessions():
    registry = TelegramConnectionRegistry()

    supervisor = registry.register("supervisor")
    worker_1 = registry.register("worker_1")
    worker_2 = registry.register("worker_2")

    supervisor.connect()
    worker_1.connect()
    worker_2.connect()

    status = get_connection_registry_status(registry)

    assert status["total_sessions"] == 3
    assert status["connected_sessions"] == 3
    assert status["disconnected_sessions"] == 0
    assert set(status["connected_bots"]) == {
        "supervisor",
        "worker_1",
        "worker_2",
  }
