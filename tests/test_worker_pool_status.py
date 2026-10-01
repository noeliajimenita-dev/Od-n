from src.workers.worker_pool_status import WorkerPoolStatus


class MockWorker:
    def __init__(self, status="idle"):
        self.status = status


def test_status_for_empty_pool():
    status_manager = WorkerPoolStatus()

    result = status_manager.get_status({})

    assert result["total"] == 0
    assert result["idle"] == 0
    assert result["working"] == 0
    assert result["paused"] == 0
    assert result["stopped"] == 0
    assert result["available"] is False


def test_status_counts_worker_states():
    status_manager = WorkerPoolStatus()

    workers = {
        "worker_1": MockWorker("idle"),
        "worker_2": MockWorker("working"),
        "worker_3": MockWorker("paused"),
        "worker_4": MockWorker("stopped"),
        "worker_5": MockWorker("idle"),
    }

    result = status_manager.get_status(workers)

    assert result["total"] == 5
    assert result["idle"] == 2
    assert result["working"] == 1
    assert result["paused"] == 1
    assert result["stopped"] == 1


def test_status_reports_worker_states():
    status_manager = WorkerPoolStatus()

    workers = {
        "worker_1": MockWorker("idle"),
        "worker_2": MockWorker("working"),
    }

    result = status_manager.get_status(workers)

    assert result["worker_statuses"] == {
        "worker_1": "idle",
        "worker_2": "working",
    }


def test_pool_is_available_when_worker_is_idle():
    status_manager = WorkerPoolStatus()

    workers = {
        "worker_1": MockWorker("working"),
        "worker_2": MockWorker("idle"),
    }

    assert status_manager.is_available(workers) is True


def test_pool_is_not_available_when_no_worker_is_idle():
    status_manager = WorkerPoolStatus()

    workers = {
        "worker_1": MockWorker("working"),
        "worker_2": MockWorker("paused"),
    }

    assert status_manager.is_available(workers) is False


def test_available_count():
    status_manager = WorkerPoolStatus()

    workers = {
        "worker_1": MockWorker("idle"),
        "worker_2": MockWorker("idle"),
        "worker_3": MockWorker("working"),
    }

    assert status_manager.available_count(workers) == 2


def test_working_count():
    status_manager = WorkerPoolStatus()

    workers = {
        "worker_1": MockWorker("working"),
        "worker_2": MockWorker("working"),
        "worker_3": MockWorker("idle"),
    }

    assert status_manager.working_count(workers) == 2


def test_unknown_status_is_counted():
    status_manager = WorkerPoolStatus()

    workers = {
        "worker_1": MockWorker("idle"),
        "worker_2": MockWorker("maintenance"),
    }

    result = status_manager.get_status(workers)

    assert result["unknown"] == 1
    assert result["idle"] == 1
