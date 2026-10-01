import pytest

from src.supervisor.task import Task
from src.supervisor.task_assignment_log import TaskAssignmentLog
from src.supervisor.task_assignment_manager import TaskAssignmentManager
from src.supervisor.task_assignment_service import TaskAssignmentService
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


def create_executor() -> WorkerTaskExecutor:
    pool = WorkerPool()

    worker = MockWorker(
        skills=["data_science"],
    )

    pool.add_worker("worker_1", worker)

    bridge = SupervisorWorkerBridge(pool)
    router = SupervisorTaskRouter(bridge)
    manager = TaskAssignmentManager(router)
    log = TaskAssignmentLog()

    service = TaskAssignmentService(
        manager=manager,
        assignment_log=log,
    )

    return WorkerTaskExecutor(service)


def create_assigned_task() -> Task:
    task = Task(
        task_id="task-001",
        description="Analyze dataset",
    )
    task.assign("worker_1")
    return task


def test_executor_requires_assignment_service():
    with pytest.raises(
        ValueError,
        match="Task assignment service is required",
    ):
        WorkerTaskExecutor(None)


def test_executor_returns_handler_result():
    executor = create_executor()
    task = create_assigned_task()
    handler = MockHandler(result="success")

    result = executor.execute(task, handler)

    assert result == "success"


def test_executor_completes_task_after_success():
    executor = create_executor()
    task = create_assigned_task()
    handler = MockHandler(result="completed")

    executor.execute(task, handler)

    assert task.status == "completed"
    assert task.metadata["result"] == "completed"


def test_executor_records_start_and_completion_events():
    executor = create_executor()
    task = create_assigned_task()
    handler = MockHandler(result="ok")

    executor.execute(task, handler)

    events = executor.assignment_service.get_task_events(
        "task-001",
    )

    assert [event.event for event in events] == [
        "started",
        "completed",
    ]


def test_executor_marks_task_failed_on_error():
    executor = create_executor()
    task = create_assigned_task()
    handler = MockHandler(
        error=RuntimeError("execution failed"),
    )

    with pytest.raises(
        RuntimeError,
        match="execution failed",
    ):
        executor.execute(task, handler)

    assert task.status == "failed"
    assert task.metadata["error"] == "execution failed"


def test_executor_records_failure_event():
    executor = create_executor()
    task = create_assigned_task()
    handler = MockHandler(
        error=RuntimeError("execution failed"),
    )

    with pytest.raises(RuntimeError):
        executor.execute(task, handler)

    events = executor.assignment_service.get_task_events(
        "task-001",
    )

    assert [event.event for event in events] == [
        "started",
        "failed",
    ]


def test_executor_rejects_invalid_task():
    executor = create_executor()
    handler = MockHandler(result="success")

    with pytest.raises(
        TypeError,
        match="Expected a Task instance",
    ):
        executor.execute("invalid_task", handler)


def test_executor_rejects_unassigned_task():
    executor = create_executor()
    task = Task(
        task_id="task-002",
        description="Unassigned task",
    )
    handler = MockHandler(result="success")

    with pytest.raises(
        ValueError,
        match="Task must be assigned to a worker",
    ):
        executor.execute(task, handler)


def test_executor_rejects_missing_handler():
    executor = create_executor()
    task = create_assigned_task()

    with pytest.raises(
        ValueError,
        match="A valid execution handler is required",
    ):
        executor.execute(task, None)


def test_executor_handler_receives_running_task():
    executor = create_executor()
    task = create_assigned_task()

    class StatusHandler:
        def execute(self, current_task):
            assert current_task.status == "running"
            return "ok"

    result = executor.execute(
        task,
        StatusHandler(),
    )

    assert result == "ok"
    assert task.status == "completed"
