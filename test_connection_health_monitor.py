from src.telegram.connection_registry import TelegramConnectionRegistry
from src.telegram.connection_health_monitor import (
    TelegramConnectionHealthMonitor,
)


def test_monitor_detects_healthy_and_unhealthy_bots():
    registry = TelegramConnectionRegistry()

    supervisor = registry.register("supervisor")
    registry.register("worker_1")
    worker_2 = registry.register("worker_2")

    supervisor.connect()
    worker_2.connect()

    monitor = TelegramConnectionHealthMonitor(registry)

    results = monitor.check_all()

    assert results["supervisor"]["healthy"] is True
    assert results["worker_1"]["healthy"] is False
    assert results["worker_2"]["healthy"] is True


def test_monitor_lists_unhealthy_bots():
    registry = TelegramConnectionRegistry()

    registry.register("supervisor")
    worker_1 = registry.register("worker_1")

    worker_1.connect()

    monitor = TelegramConnectionHealthMonitor(registry)

    unhealthy = monitor.unhealthy_bots()

    assert unhealthy == ["supervisor"]


def test_monitor_reports_all_healthy():
    registry = TelegramConnectionRegistry()

    supervisor = registry.register("supervisor")
    worker_1 = registry.register("worker_1")

    supervisor.connect()
    worker_1.connect()

    monitor = TelegramConnectionHealthMonitor(registry)

    assert monitor.all_healthy() is True


def test_monitor_reports_not_all_healthy():
    registry = TelegramConnectionRegistry()

    registry.register("supervisor")

    monitor = TelegramConnectionHealthMonitor(registry)

    assert monitor.all_healthy() is False


def test_monitor_empty_registry():
    registry = TelegramConnectionRegistry()

    monitor = TelegramConnectionHealthMonitor(registry)

    assert monitor.check_all() == {}
    assert monitor.unhealthy_bots() == []
    assert monitor.all_healthy() is True
