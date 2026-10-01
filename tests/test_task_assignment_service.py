import pytest

from src.supervisor.task import Task
from src.supervisor.task_assignment_log import TaskAssignmentLog
from src.supervisor.task_assignment_manager import TaskAssignmentManager
from src.supervisor.task_assignment_service import TaskAssignmentService
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


def create_service() -> tuple[
    TaskAssignmentService,
    MockWorker,
    MockWorker,
]:
    pool = WorkerPool()

    worker_1 = MockWorker(skills=["data_science"])
    worker_2 = MockWorker(skills=["cybersecurity"])

    pool.add_worker("worker_1", worker_1)
    pool.add_worker("worker_2", worker_2)

    bridge = SupervisorWorkerBridge(pool)
    router = SupervisorTaskRouter(bridge)
    manager = TaskAssignmentManager(router)
    log = TaskAssignmentLog()

    service = TaskAssignmentService(
        manager=manager,
        assignment_log=log,
    )

    return service, worker_1, worker_2


def test_service_requires_manager():
    with pytest.raises(
        ValueError,
        match="Task assignment manager is required",
    ):
        TaskAssignmentService(None)


def test_service_assigns_task():
    service, worker_1, _ = create_service()

    task = Task(
        task_id="task-001",
        description="Data analysis",
    )

    result = service.assign(task)

    assert result is worker_1
    assert task.bot_name == "worker_1"
    assert task.status == "assigned"


def test_service_logs_assignment_automatically():
    service, _, _ = create_service()

    task = Task(
        task_id="task-002",
        description="Security analysis",
    )

    service.assign(
        task,
        required_skill="cybersecurity",
    )

    events = service.get_task_events("task-002")

    assert len(events) == 1
    assert events[0].task_id == "task-002"
    assert events[0].worker_id == "worker_2"
    assert events[0].event == "assigned"


def test_service_assigns_using_required_skill():
    service, _, worker_2 = create_service()

    task = Task(
        task_id="task-003",
        description="Security task",
    )

    result = service.assign(
        task,
        required_skill="cybersecurity",
    )

    assert result is worker_2
    assert service.get_assignment("task-003") == "worker_2"


def test_service_records_additional_event():
    service, _, _ = create_service()

    task = Task(
        task_id="task-004",
        description="Test task",
    )

    service.assign(task)
    event = service.record_event(task, "started")

    assert event.task_id == "task-004"
    assert event.worker_id == "worker_1"
    assert event.event == "started"


def test_service_returns_task_events():
    service, _, _ = create_service()

    task = Task(
        task_id="task-005",
        description="Tracked task",
    )

    service.assign(task)
    service.record_event(task, "started")
    service.record_event(task, "completed")

    events = service.get_task_events("task-005")

    assert [event.event for event in events] == [
        "assigned",
        "started",
        "completed",
    ]


def test_service_returns_worker_events():
    service, _, worker_2 = create_service()

    task = Task(
        task_id="task-006",
        description="Security task",
    )

    service.assign(
        task,
        required_skill="cybersecurity",
    )
    service.record_event(task, "started")

    events = service.get_worker_events("worker_2")

    assert len(events) == 2
    assert all(event.worker_id == "worker_2" for event in events)


def test_service_rejects_invalid_task():
    service, _, _ = create_service()

    with pytest.raises(
        TypeError,
        match="Expected a Task instance",
    ):
        service.assign("invalid_task")


def test_service_rejects_event_for_invalid_task():
    service, _, _ = create_service()

    with pytest.raises(
        TypeError,
        match="Expected a Task instance",
    ):
        service.record_event("invalid_task", "started")


def test_service_rejects_event_without_worker():
    service, _, _ = create_service()

    task = Task(
        task_id="task-007",
        description="Unassigned task",
    )

    with pytest.raises(
        RuntimeError,
        match="Task has no assigned worker",
    ):
        service.record_event(task, "started")


def test_service_reports_assignment_and_event_counts
