import pytest

from src.supervisor.task import Task
from src.supervisor.task_assignment_manager import TaskAssignmentManager
from src.supervisor.task_router import SupervisorTaskRouter
from src.supervisor.worker_bridge import SupervisorWorkerBridge
from src.workers.worker_pool import WorkerPool


class MockWorker:
    def __init__(self, skills=None, status="idle"):
        self.skills = skills or []
        self.status = status
        self.pending_tasks = []
        self.current_task = None

    def can_handle(self, skill: str) -> bool:
        return skill in self.skills


def create_manager() -> tuple[TaskAssignmentManager, MockWorker, MockWorker]:
    pool = WorkerPool()

    worker_1 = MockWorker(skills=["data_science"])
    worker_2 = MockWorker(skills=["cybersecurity"])

    pool.add_worker("worker_1", worker_1)
    pool.add_worker("worker_2", worker_2)

    bridge = SupervisorWorkerBridge(pool)
    router = SupervisorTaskRouter(bridge)
    manager = TaskAssignmentManager(router)

    return manager, worker_1, worker_2


def test_manager_requires_router():
    with pytest.raises(ValueError, match="Task router is required"):
        TaskAssignmentManager(None)


def test_manager_assigns_task():
    manager, worker_1, _ = create_manager()

    task = Task(
        task_id="task-001",
        description="Data analysis",
    )

    result = manager.assign(task)

    assert result is worker_1
    assert task.bot_name == "worker_1"
    assert manager.is_assigned("task-001") is True


def test_manager_tracks_assignment():
    manager, _, worker_2 = create_manager()

    task = Task(
        task_id="task-002",
        description="Security analysis",
    )

    manager.assign(
        task,
        required_skill="cybersecurity",
    )

    assert manager.get_assignment("task-002") == "worker_2"
    assert worker_2 is not None


def test_manager_assigns_using_required_skill():
    manager, _, worker_2 = create_manager()

    task = Task(
        task_id="task-003",
        description="Security task",
    )

    result = manager.assign(
        task,
        required_skill="cybersecurity",
    )

    assert result is worker_2
    assert manager.get_assignment("task-003") == "worker_2"


def test_manager_returns_none_for_unknown_assignment():
    manager, _, _ = create_manager()

    assert manager.get_assignment("unknown-task") is None
    assert manager.is_assigned("unknown-task") is False


def test_manager_removes_assignment():
    manager, _, _ = create_manager()

    task = Task(
        task_id="task-004",
        description="Test task",
    )

    manager.assign(task)

    removed = manager.remove_assignment("task-004")

    assert removed == "worker_1"
    assert manager.is_assigned("task-004") is False
    assert manager.count() == 0


def test_manager_remove_unknown_assignment():
    manager, _, _ = create_manager()

    assert manager.remove_assignment("unknown-task") is None


def test_manager_lists_assignments():
    manager, _, worker_2 = create_manager()

    task_1 = Task(
        task_id="task-001",
        description="Data task",
    )
    task_2 = Task(
        task_id="task-002",
        description="Security task",
    )

    manager.assign(task_1)
    manager.assign(task_2, required_skill="cybersecurity")

    assignments = manager.list_assignments()

    assert assignments == {
        "task-001": "worker_1",
        "task-002": "worker_2",
    }


def test_manager_count():
    manager, _, _ = create_manager()

    task_1 = Task(
        task_id="task-001",
        description="First task",
    )
    task_2 = Task(
        task_id="task-002",
        description="Second task",
    )

    manager.assign(task_1)
    manager.assign(task_2)

    assert manager.count() == 2


def test_manager_rejects_invalid_task():
    manager, _, _ = create_manager()

    with pytest.raises(TypeError, match="Expected a Task instance"):
        manager.assign("invalid_task")
