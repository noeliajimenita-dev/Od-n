from src.workers.worker_coordinator import WorkerCoordinator


class MockWorker:
    def __init__(self, status="idle", skills=None, pending_tasks=None):
        self.status = status
        self.skills = skills or []
        self.pending_tasks = pending_tasks or []
        self.current_task = None

    def can_handle(self, skill: str) -> bool:
        return skill in self.skills


def test_coordinator_starts_empty():
    coordinator = WorkerCoordinator()

    assert coordinator.worker_count() == 0
    assert coordinator.list_workers() == []


def test_coordinator_registers_worker():
    coordinator = WorkerCoordinator()
    worker = MockWorker()

    coordinator.register_worker("worker_1", worker)

    assert coordinator.worker_count() == 1
    assert coordinator.get_worker("worker_1") is worker


def test_coordinator_lists_registered_workers():
    coordinator = WorkerCoordinator()

    coordinator.register_worker("worker_1", MockWorker())
    coordinator.register_worker("worker_2", MockWorker())

    assert coordinator.list_workers() == ["worker_1", "worker_2"]


def test_coordinator_selects_worker_by_skill():
    coordinator = WorkerCoordinator()

    worker_1 = MockWorker(skills=["data_science"])
    worker_2 = MockWorker(skills=["cybersecurity"])

    coordinator.register_worker("worker_1", worker_1)
    coordinator.register_worker("worker_2", worker_2)

    result = coordinator.select_worker("cybersecurity")

    assert result is worker_2


def test_coordinator_returns_none_when_skill_is_unavailable():
    coordinator = WorkerCoordinator()

    coordinator.register_worker(
        "worker_1",
        MockWorker(skills=["data_science"]),
    )

    assert coordinator.select_worker("graphic_design") is None


def test_coordinator_assigns_least_loaded_worker():
    coordinator = WorkerCoordinator()

    worker_1 = MockWorker(
        skills=["data_science"],
        pending_tasks=["task-1", "task-2"],
    )
    worker_2 = MockWorker(
        skills=["data_science"],
        pending_tasks=[],
    )

    coordinator.register_worker("worker_1", worker_1)
    coordinator.register_worker("worker_2", worker_2)

    result = coordinator.assign_worker("data_science")

    assert result is worker_2


def test_coordinator_skips_busy_worker():
    coordinator = WorkerCoordinator()

    busy_worker = MockWorker(
        status="working",
        skills=["cybersecurity"],
    )
    idle_worker = MockWorker(
        status="idle",
        skills=["data_science"],
    )

    coordinator.register_worker("worker_1", busy_worker)
    coordinator.register_worker("worker_2", idle_worker)

    result = coordinator.assign_worker("cybersecurity")

    assert result is None


def test_coordinator_removes_worker():
    coordinator = WorkerCoordinator()
    worker = MockWorker()

    coordinator.register_worker("worker_1", worker)

    removed = coordinator.remove_worker("worker_1")

    assert removed is worker
    assert coordinator.get_worker("worker_1") is None
    assert coordinator.worker_count() == 0


def test_coordinator_returns_none_for_unknown_worker():
    coordinator = WorkerCoordinator()

    assert coordinator.get_worker("worker_unknown") is None


def test_coordinator_rejects_duplicate_worker():
    coordinator = WorkerCoordinator()

    coordinator.register_worker("worker_1", MockWorker())

    try:
        coordinator.register_worker("worker_1", MockWorker())
        assert False
    except ValueError:
        assert True
