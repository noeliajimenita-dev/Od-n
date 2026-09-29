from src.telegram.connection_registry import TelegramConnectionRegistry
from src.telegram.connection_health_status import (
    get_connection_health_status,
)


def test_health_status_empty_registry():
    registry = TelegramConnectionRegistry()

    status = get_connection_health_status(registry)

    assert status["total_bots"] == 0
    assert status["healthy_bots"] == 0
    assert status["unhealthy_bots"] == 0
    assert status["healthy_bot_names"] == []
    assert status["unhealthy_bot_names"] == []


def test_health_status_with_disconnected_bots():
    registry = TelegramConnectionRegistry()

    registry.register("supervisor")
    registry.register("worker_1")

    status = get_connection_health_status(registry)

    assert status["total_bots"] == 2
    assert status["healthy_bots"] == 0
    assert status["unhealthy_bots"] == 2
    assert status["healthy_bot_names"] == []
    assert set(status["unhealthy_bot_names"]) == {
        "supervisor",
        "worker_1",
    }


def test_health_status_with_connected_and_disconnected_bots():
    registry = TelegramConnectionRegistry()

    supervisor = registry.register("supervisor")
    registry.register("worker_1")
    worker_2 = registry.register("worker_2")

    supervisor.connect()
    worker_2.connect()

    status = get_connection_health_status(registry)

    assert status["total_bots"] == 3
    assert status["healthy_bots"] == 2
    assert status["unhealthy_bots"] == 1

    assert set(status["healthy_bot_names"]) == {
        "supervisor",
        "worker_2",
    }

    assert status["unhealthy_bot_names"] == ["worker_1"]
