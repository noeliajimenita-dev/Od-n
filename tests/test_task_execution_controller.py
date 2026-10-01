import pytest

from src.supervisor.task import Task
from src.supervisor.task_assignment_log import TaskAssignmentLog
from src.supervisor.task_assignment_manager import TaskAssignmentManager
from src.supervisor.task_assignment_service import TaskAssignmentService
from src.supervisor.task_execution_controller import TaskExecutionController
from src.supervisor.task_lifecycle_manager import TaskLifecycleManager
from src.supervisor.task_router import SupervisorTaskRouter
from src.supervisor.worker_bridge import SupervisorWorkerBridge
from src.supervisor.worker_task_executor import WorkerTaskExecutor
from src.workers.worker_pool import WorkerPool


class MockWorker:
    def __init__(self, skills=None, status="idle"):
        self.skills = skills or []
        self.status = status
        self.pending_tasks = []
        self.current_task = None

    def can_handle(self, skill: str) -> bool:
        return skill in self.skills


class MockHandler:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error

    def execute(self, task):
        if self.error is not None:
            raise self.error
        return self.result


def create_controller() -> TaskExecutionController:
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

    lifecycle_manager = TaskLifecycleManager(
        assignment_service,
    )

    worker_executor = WorkerTaskExecutor(
        assignment_service,
    )

    return TaskExecutionController(
        lifecycle_manager=lifecycle_manager,
        worker_executor=worker_executor,
    )


def create_assigned_task() -> Task:
    task = Task(
        task_id="task-001",
        description="Analyze dataset",
    )
    task.assign("worker_1")
    return task


def test_controller_requires_lifecycle_manager():
    controller = object.__new__(TaskExecutionController)

    with pytest.raises(
        ValueError,
        match="Task lifecycle manager is required",
    ):
        TaskExecutionController(
            lifecycle_manager=None,
            worker_executor=object(),
        )


def test_controller_requires_worker_executor():
    with pytest.raises(
        ValueError,
        match="Worker task executor is required",
    ):
        TaskExecutionController(
            lifecycle_manager=object(),
            worker_executor=None,
        )


def test_controller_executes_assigned_task():
    controller = create_controller()
    task = create_assigned_task()
    handler = MockHandler(result="success")

    result = controller.execute(task, handler)

    assert result == "success"
    assert task.status == "completed"
    assert task.metadata["result"] == "success"


def test_controller_records_lifecycle_events():
    controller = create_controller()
    task = create_assigned_task()
    handler = MockHandler(result="completed")

    controller.execute(task, handler)

    events = (
        controller
        .lifecycle_manager
        .assignment_service
        .get_task_events("task-001")
    )

    assert [event.event for event in events] == [
        "started",
        "completed",
    ]


def test_controller_marks_task_failed():
    controller = create_controller()
    task = create_assigned_task()
    handler = MockHandler(
        error=RuntimeError("worker failed"),
    )

    with pytest.raises(
        RuntimeError,
        match="worker failed",
    ):
        controller.execute(task, handler)

    assert task.status == "failed"
    assert task.metadata["error"] == "worker failed"


def test_controller_records_failure_event():
    controller = create_controller()
    task = create_assigned_task()
    handler = MockHandler(
        error=RuntimeError("worker failed"),
    )

    with pytest.raises(RuntimeError):
        controller.execute(task, handler)

    events = (
        controller
        .lifecycle_manager
        .assignment_service
        .get_task_events("task-001")
    )

    assert [event.event for event in events] == [
        "started",
        "failed",
    ]


def test_controller_rejects_invalid_task():
    controller = create_controller()
    handler = MockHandler(result="success")

    with pytest.raises(
        TypeError,
        match="Expected a Task instance",
    ):
        controller.execute("invalid_task", handler)


def test_controller_rejects_unassigned_task():
    controller = create_controller()

    task = Task(
        task_id="task-002",
        description="Unassigned task",
    )

    handler = MockHandler(result="success")
