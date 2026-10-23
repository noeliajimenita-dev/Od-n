import pytest

from src.supervisor.task import Task
from src.supervisor.task_assignment_service import TaskAssignmentService
from src.supervisor.task_execution_controller import TaskExecutionController
from src.supervisor.task_execution_orchestrator import TaskExecutionOrchestrator
from src.supervisor.task_execution_result_service import TaskExecutionResultService
from src.supervisor.task_lifecycle_manager import TaskLifecycleManager
from src.supervisor.worker_task_executor import WorkerTaskExecutor


class FakeHandler:
    def __init__(self, result="ok"):
        self.result = result

    def execute(self, task):
        return self.result


class FailingHandler:
    def execute(self, task):
        raise RuntimeError("execution failed")


def build_orchestrator():
    assignment_service = TaskAssignmentService()
    lifecycle_manager = TaskLifecycleManager(assignment_service)
    worker_executor = WorkerTaskExecutor(assignment_service)

    controller = TaskExecutionController(
        lifecycle_manager,
        worker_executor,
    )

    result_service = TaskExecutionResultService()

    orchestrator = TaskExecutionOrchestrator(
        controller,
        result_service,
    )

    return orchestrator


def build_task(task_id="task-1"):
    task = Task(
        task_id=task_id,
        description="Execute test task",
    )
    task.assign("worker_1")
    return task


def test_orchestrator_executes_task_successfully():
    orchestrator = build_orchestrator()
    task = build_task()

    result = orchestrator.execute(
        task,
        FakeHandler("completed"),
    )

    assert result.task_id == "task-1"
    assert result.status == "completed"
    assert result.output == "completed"
    assert result.is_success is True


def test_orchestrator_stores_success_result():
    orchestrator = build_orchestrator()
    task = build_task()

    orchestrator.execute(
        task,
        FakeHandler("stored"),
    )

    stored = orchestrator.get_result("task-1")

    assert stored is not None
    assert stored.output == "stored"
    assert stored.status == "completed"


def test_orchestrator_reports_failure_as_result():
    orchestrator = build_orchestrator()
    task = build_task()

    result = orchestrator.execute(
        task,
        FailingHandler(),
    )

    assert result.task_id == "task-1"
    assert result.status == "failed"
    assert result.error == "execution failed"
    assert result.is_failure is True


def test_orchestrator_stores_failure_result():
    orchestrator = build_orchestrator()
    task = build_task()

    orchestrator.execute(
        task,
        FailingHandler(),
    )

    stored = orchestrator.get_result("task-1")

    assert stored is not None
    assert stored.status == "failed"
    assert stored.error == "execution failed"


def test_orchestrator_has_result():
    orchestrator = build_orchestrator()
    task = build_task()

    assert orchestrator.has_result("task-1") is False

    orchestrator.execute(
        task,
        FakeHandler("ok"),
    )

    assert orchestrator.has_result("task-1") is True


def test_orchestrator_summary_counts_success_and_failure():
    orchestrator = build_orchestrator()

    successful_task = build_task("task-success")
    failed_task = build_task("task-failure")

    orchestrator.execute(
        successful_task,
        FakeHandler("ok"),
    )

    orchestrator.execute(
        failed_task,
        FailingHandler(),
    )

    summary = orchestrator.summary()

    assert summary == {
        "total": 2,
        "completed": 1,
        "failed": 1,
    }


def test_orchestrator_rejects_invalid_task():
    orchestrator = build_orchestrator()

    with pytest.raises(TypeError):
        orchestrator.execute(
            "invalid-task",
            FakeHandler(),
        )


def test_orchestrator_rejects_unassigned_task():
    orchestrator = build_orchestrator()

    task = Task(
        task_id="unassigned",
        description="Task without worker",
    )

    result = orchestrator.execute(
        task,
        FakeHandler(),
    )

    assert result.status == "failed"
    assert "assigned" in result.error.lower()


def test_orchestrator_get_missing_result_returns_none():
    orchestrator = build_orchestrator()
    result = orchestrator.get_result("non-existent-task")
    assert result is None
