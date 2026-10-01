import pytest

from src.supervisor.task import Task
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


def create_router() -> tuple[SupervisorTaskRouter, MockWorker, MockWorker]:
    pool = WorkerPool()

    worker_1 = MockWorker(skills=["data_science"])
    worker_2 = MockWorker(skills=["cybersecurity"])

    pool.add_worker("worker_1", worker_1)
    pool.add_worker("worker_2", worker_2)

    bridge = SupervisorWorkerBridge(pool)
    router = SupervisorTaskRouter(bridge)

    return router, worker_1, worker_2


def test_router_requires_bridge():
    with pytest.raises(
        ValueError,
        match="Supervisor worker bridge is required",
    ):
        SupervisorTaskRouter(None)


def test_router_assigns_task_without_required_skill():
    router, worker_1, _ = create_router()

    task = Task(
        task_id="task-001",
        description="General task",
    )

    result = router.route(task)

    assert result is worker_1
    assert task.bot_name == "worker_1"


def test_router_uses_required_skill_from_metadata():
    router, _, worker_2 = create_router()

    task = Task(
        task_id="task-002",
        description="Security task",
        metadata={"required_skill": "cybersecurity"},
    )

    result = router.route(task)

    assert result is worker_2
    assert task.bot_name == "worker_2"


def test_router_with_skill_assigns_correct_worker():
    router, _, worker_2 = create_router()

    task = Task(
        task_id="task-003",
        description="Security analysis",
    )

    result = router.route_with_skill(
        task,
        "cybersecurity",
    )

    assert result is worker_2
    assert task.bot_name == "worker_2"
    assert task.metadata["required_skill"] == "cybersecurity"


def test_router_normalizes_skill():
    router, _, worker_2 = create_router()

    task = Task(
        task_id="task-004",
        description="Security analysis",
    )

    result = router.route_with_skill(
        task,
        "  CYBERSECURITY  ",
    )

    assert result is worker_2
    assert task.metadata["required_skill"] == "cybersecurity"


def test_router_rejects_invalid_task():
    router, _, _ = create_router()

    with pytest.raises(TypeError, match="Expected a Task instance"):
        router.route("invalid_task")


def test_router_with_skill_rejects_invalid_task():
    router, _, _ = create_router()

    with pytest.raises(TypeError, match="Expected a Task instance"):
        router.route_with_skill("invalid_task", "data_science")


def test_router_rejects_empty_skill():
    router, _, _ = create_router()

    task = Task(
        task_id="task-005",
        description="Invalid skill",
    )

    with pytest.raises(ValueError, match="Skill cannot be empty"):
        router.route_with_skill(task, "   ")


def test_router_fails_when_required_skill_is_unavailable():
    router, _, _ = create_router()

    task = Task(
        task_id="task-006",
        description="Design task",
        metadata={"required_skill": "graphic_design"},
    )

    with pytest.raises(
        RuntimeError,
        match="No suitable worker available",
    ):
        router.route(task)
