import pytest

from src.supervisor.task import Task
from src.supervisor.task_assignment_log import TaskAssignmentLog
from src.supervisor.task_assignment_manager import TaskAssignmentManager
from src.supervisor.task_assignment_service import TaskAssignmentService
from src.supervisor.task_lifecycle_manager import TaskLifecycleManager
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


def create_manager() -> TaskLifecycleManager:
    pool = WorkerPool()

    worker = MockWorker(
        skills=["data_science"],
    )

    pool.add_worker("worker_1", worker)

    bridge = SupervisorWorkerBridge(pool)
    router = SupervisorTaskRouter(bridge)
    assignment_manager = TaskAssignmentManager(router)
    assignment_log = TaskAssignmentLog()

    assignment_service = TaskAssignmentService(
        manager=assignment_manager,
        assignment_log=assignment_log,
    )

    return TaskLifecycleManager(assignment_service)


def create_assigned_task() -> Task:
    task = Task(
        task_id="task-001",
        description="Analyze dataset",
    )
    task.assign("worker_1")
    return task


def test_manager_requires_assignment_service():
    with pytest.raises(
        ValueError,
        match="Task assignment service is required",
    ):
        TaskLifecycleManager(None)


def test_start_changes_task_to_running():
    manager = create_manager()
    task = create_assigned_task()

    manager.start(task)

    assert task.status == "running"


def test_start_records_event():
    manager = create_manager()
    task = create_assigned_task()

    manager.start(task)

    events = manager.assignment_service.get_task_events(
        "task-001",
    )

    assert len(events) == 1
    assert events[0].event == "started"


def test_complete_changes_task_to_completed():
    manager = create_manager()
    task = create_assigned_task()

    manager.start(task)
    manager.complete(task, "success")

    assert task.status == "completed"
    assert task.metadata["result"] == "success"


def test_complete_records_event():
    manager = create_manager()
    task = create_assigned_task()

    manager.start(task)
    manager.complete(task)

    events = manager.assignment_service.get_task_events(
        "task-001",
    )

    assert [event.event for event in events] == [
        "started",
        "completed",
    ]


def test_fail_changes_task_to_failed():
    manager = create_manager()
    task = create_assigned_task()

    manager.start(task)
    manager.fail(task, "Worker execution failed")

    assert task.status == "failed"
    assert task.metadata["error"] == "Worker execution failed"


def test_fail_records_event():
    manager = create_manager()
    task = create_assigned_task()

    manager.start(task)
    manager.fail(task, "Execution error")

    events = manager.assignment_service.get_task_events(
        "task-001",
    )

    assert [event.event for event in events] == [
        "started",
        "failed",
    ]


def test_start_rejects_unassigned_task():
    manager = create_manager()

    task = Task(
        task_id="task-002",
        description="Unassigned task",
    )

    with pytest.raises(
        ValueError,
        match="Task must be assigned to a worker",
    ):
        manager.start(task)


def test_start_rejects_task_not_in_assigned_state():
    manager = create_manager()
    task = create_assigned_task()

    task.status = "completed"

    with pytest.raises(
        ValueError,
        match="Task must be assigned before it can start",
    ):
        manager.start(task)


def test_complete_rejects_task_not_running():
    manager = create_manager()
    task = create_assigned_task()

    with pytest.raises(
        ValueError,
        match="Task
