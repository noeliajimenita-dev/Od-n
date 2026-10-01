import pytest

from src.supervisor.task import Task
from src.supervisor.worker_bridge import SupervisorWorkerBridge
from src.workers.worker_pool import WorkerPool


class MockWorker:
    def __init__(self, status="idle", skills=None):
        self.status = status
        self.skills = skills or []
        self.pending_tasks = []
        self.current_task = None

    def can_handle(self, skill: str) -> bool:
        return skill in self.skills


def create_pool() -> tuple[WorkerPool, MockWorker, MockWorker]:
    pool = WorkerPool()

    worker_1 = MockWorker(skills=["data_science"])
    worker_2 = MockWorker(skills=["cybersecurity"])

    pool.add_worker("worker_1", worker_1)
    pool.add_worker("worker_2", worker_2)

    return pool, worker_1, worker_2


def test_bridge_requires_worker_pool():
    with pytest.raises(ValueError, match="Worker pool is required"):
        SupervisorWorkerBridge(None)


def test_bridge_assigns_task_to_available_worker():
    pool, worker_1, _ = create_pool()
    bridge = SupervisorWorkerBridge(pool)

    task = Task(
        task_id="task-001",
        description="Analyze dataset",
    )

    result = bridge.assign_task(task)

    assert result is worker_1
    assert task.bot_name == "worker_1"
    assert task.status == "assigned"


def test_bridge_selects_worker_by_required_skill():
    pool, _, worker_2 = create_pool()
    bridge = SupervisorWorkerBridge(pool)

    task = Task(
        task_id="task-002",
        description="Security analysis",
    )

    result = bridge.assign_task(
        task,
        required_skill="cybersecurity",
    )

    assert result is worker_2
    assert task.bot_name == "worker_2"


def test_bridge_rejects_invalid_task():
    pool, _, _ = create_pool()
    bridge = SupervisorWorkerBridge(pool)

    with pytest.raises(TypeError, match="Expected a Task instance"):
        bridge.assign_task("invalid_task")


def test_bridge_rejects_task_when_no_worker_is_available():
    pool = WorkerPool()

    busy_worker = MockWorker(
        status="working",
        skills=["data_science"],
    )

    pool.add_worker("worker_1", busy_worker)

    bridge = SupervisorWorkerBridge(pool)

    task = Task(
        task_id="task-003",
        description="Busy worker test",
    )

    with pytest.raises(
        RuntimeError,
        match="No suitable worker available",
    ):
        bridge.assign_task(task)


def test_bridge_rejects_missing_skill():
    pool, _, _ = create_pool()
    bridge = SupervisorWorkerBridge(pool)

    task = Task(
        task_id="task-004",
        description="Design task",
    )

    with pytest.raises(
        RuntimeError,
        match="No suitable worker available",
    ):
        bridge.assign_task(
            task,
            required_skill="graphic_design",
        )


def test_bridge_assigns_registered_worker_id_to_task():
    pool, _, worker_2 = create_pool()
    bridge = SupervisorWorkerBridge(pool)

    task = Task(
        task_id="task-005",
        description="Cybersecurity task",
    )

    bridge.assign_task(
        task,
        required_skill="cybersecurity",
    )

    assert task.bot_name == "worker_2"
    assert pool.get_worker(task.bot_name) is worker_2


def test_bridge_can_assign_multiple_tasks():
    pool, worker_1, _ = create_pool()
    bridge = SupervisorWorkerBridge(pool)

    first_task = Task(
        task_id="task-001",
        description="First task",
    )
    second_task = Task(
        task_id="task-002",
        description="Second task",
    )

    first_worker = bridge.assign_task(first_task)
    second_worker = bridge.assign_task(second_task)

    assert first_worker is worker_1
    assert second_worker is worker_1
    assert first_task.status == "assigned"
    assert second_task.status == "assigned"
