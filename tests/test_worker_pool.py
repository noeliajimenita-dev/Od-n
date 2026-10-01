from src.workers.worker_pool import WorkerPool


class MockWorker:
    def __init__(
        self,
        status="idle",
        skills=None,
        pending_tasks=None,
    ):
        self.status = status
        self.skills = skills or []
        self.pending_tasks = pending_tasks or []
        self.current_task = None

    def can_handle(self, skill: str) -> bool:
        return skill in self.skills


def test_pool_starts_empty():
    pool = WorkerPool()

    assert pool.count() == 0
    assert pool.list_workers() == []


def test_pool_adds_worker():
    pool = WorkerPool()
    worker = MockWorker()

    pool.add_worker("worker_1", worker)

    assert pool.count() == 1
    assert pool.get_worker("worker_1") is worker


def test_pool_removes_worker():
    pool = WorkerPool()
    worker = MockWorker()

    pool.add_worker("worker_1", worker)

    removed = pool.remove_worker("worker_1")

    assert removed is worker
    assert pool.count() == 0


def test_pool_selects_worker_by_skill():
    pool = WorkerPool()

    worker_1 = MockWorker(skills=["data_science"])
    worker_2 = MockWorker(skills=["cybersecurity"])

    pool.add_worker("worker_1", worker_1)
    pool.add_worker("worker_2", worker_2)

    result = pool.select_worker("cybersecurity")

    assert result is worker_2


def test_pool_assigns_least_loaded_worker():
    pool = WorkerPool()

    worker_1 = MockWorker(
        skills=["data_science"],
        pending_tasks=["task-1", "task-2"],
    )
    worker_2 = MockWorker(
        skills=["data_science"],
        pending_tasks=[],
    )

    pool.add_worker("worker_1", worker_1)
    pool.add_worker("worker_2", worker_2)

    result = pool.assign_worker("data_science")

    assert result is worker_2


def test_pool_status_reports_workers():
    pool = WorkerPool()

    pool.add_worker(
        "worker_1",
        MockWorker(status="idle"),
    )
    pool.add_worker(
        "worker_2",
        MockWorker(status="working"),
    )

    status = pool.status()

    assert status["total"] == 2
    assert status["idle"] == 1
    assert status["working"] == 1


def test_pool_detects_available_worker():
    pool = WorkerPool()

    pool.add_worker(
        "worker_1",
        MockWorker(status="idle"),
    )

    assert pool.has_available_worker() is True


def test_pool_detects_no_available_worker():
    pool = WorkerPool()

    pool.add_worker(
        "worker_1",
        MockWorker(status="working"),
    )
    pool.add_worker(
        "worker_2",
        MockWorker(status="paused"),
    )

    assert pool.has_available_worker() is False


def test_pool_handles_multiple_workers():
    pool = WorkerPool()

    for index in range(1, 6):
        pool.add_worker(
            f"worker_{index}",
            MockWorker(),
        )

    assert pool.count() == 5
    assert pool.list_workers() == [
        "worker_1",
        "worker_2",
        "worker_3",
        "worker_4",
        "worker_5",
    ]


def test_pool_returns_none_for_unknown_worker():
    pool = WorkerPool()

    assert pool.get_worker("worker_unknown") is None
