import pytest

from src.workers.worker_registry import WorkerRegistry


class MockWorker:
    pass


def test_registry_starts_empty():
    registry = WorkerRegistry()

    assert registry.count() == 0
    assert registry.list_workers() == []


def test_register_worker():
    registry = WorkerRegistry()
    worker = MockWorker()

    registry.register("worker_1", worker)

    assert registry.has("worker_1") is True
    assert registry.count() == 1


def test_get_registered_worker():
    registry = WorkerRegistry()
    worker = MockWorker()

    registry.register("worker_1", worker)

    assert registry.get("worker_1") is worker


def test_get_unknown_worker_returns_none():
    registry = WorkerRegistry()

    assert registry.get("worker_unknown") is None


def test_remove_worker():
    registry = WorkerRegistry()
    worker = MockWorker()

    registry.register("worker_1", worker)

    removed = registry.remove("worker_1")

    assert removed is worker
    assert registry.has("worker_1") is False
    assert registry.count() == 0


def test_remove_unknown_worker_returns_none():
    registry = WorkerRegistry()

    assert registry.remove("worker_unknown") is None


def test_list_workers():
    registry = WorkerRegistry()

    registry.register("worker_1", MockWorker())
    registry.register("worker_2", MockWorker())

    assert registry.list_workers() == ["worker_1", "worker_2"]


def test_duplicate_worker_is_rejected():
    registry = WorkerRegistry()

    registry.register("worker_1", MockWorker())

    with pytest.raises(ValueError, match="already registered"):
        registry.register("worker_1", MockWorker())


def test_empty_worker_id_is_rejected():
    registry = WorkerRegistry()

    with pytest.raises(ValueError, match="Worker ID cannot be empty"):
        registry.register("   ", MockWorker())


def test_none_worker_is_rejected():
    registry = WorkerRegistry()

    with pytest.raises(ValueError, match="Worker cannot be None"):
        registry.register("worker_1", None)


def test_clear_removes_all_workers():
    registry = WorkerRegistry()

    registry.register("worker_1", MockWorker())
    registry.register("worker_2", MockWorker())
    registry.register("worker_3", MockWorker())

    registry.clear()

    assert registry.count() == 0
    assert registry.list_workers() == []
