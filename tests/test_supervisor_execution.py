from __future__ import annotations

import pytest

from src.execution.odin_execution_engine import OdinExecutionEngine
from src.execution.odin_execution_status import OdinExecutionStatus
from src.execution.supervisor_execution_controller import (
    SupervisorExecutionController,
)
from src.execution.supervisor_execution_orchestrator import (
    SupervisorExecutionOrchestrator,
)
from src.execution.supervisor_execution_result_service import (
    SupervisorExecutionResultService,
)
from src.execution.supervisor_execution_service import (
    SupervisorExecutionService,
)
from src.execution.worker_execution_adapter import (
    WorkerExecutionAdapter,
)
from src.execution.worker_execution_coordinator import (
    WorkerExecutionCoordinator,
)
from src.execution.worker_execution_registry import (
    WorkerExecutionRegistry,
)
from src.supervisor.task import Task


class FakeWorker:
    def __init__(self, worker_id: str) -> None:
        self.worker_id = worker_id
        self.tasks = []

    def execute(self, task: Task):
        self.tasks.append(task.task_id)
        return {
            "worker_id": self.worker_id,
            "task_id": task.task_id,
            "status": "done",
        }


class FailingWorker:
    def execute(self, task: Task):
        raise RuntimeError("worker execution failed")


def build_system(worker_id: str = "worker_1"):
    worker = FakeWorker(worker_id)

    registry = WorkerExecutionRegistry()
    registry.register(
        WorkerExecutionAdapter(
            worker_id=worker_id,
            worker=worker,
        )
    )

    coordinator = WorkerExecutionCoordinator(
        registry=registry,
    )

    engine = OdinExecutionEngine(
        worker_pool=None,
    )

    engine.register_handler(
        worker_id=worker_id,
        handler=worker,
    )

    service = SupervisorExecutionService(
        execution_engine=engine,
        coordinator=coordinator,
    )

    controller = SupervisorExecutionController(
        execution_service=service,
    )

    result_service = SupervisorExecutionResultService()

    orchestrator = SupervisorExecutionOrchestrator(
        controller=controller,
        result_service=result_service,
    )

    status = OdinExecutionStatus(
        orchestrator=orchestrator,
    )

    return (
        worker,
        registry,
        coordinator,
        engine,
        service,
        controller,
        result_service,
        orchestrator,
        status,
    )


def test_task_can_be_assigned_to_worker():
    (
        _,
        _,
        _,
        _,
        service,
        _,
        _,
        _,
        _,
    ) = build_system()

    task = Task(
        task_id="task-1",
        description="Test task",
    )

    worker_id = service.assign(task)

    assert worker_id == "worker_1"
    assert task.bot_name == "worker_1"
    assert task.status == "assigned"


def test_task_can_be_executed():
    (
        worker,
        _,
        _,
        _,
        _,
        _,
        _,
        orchestrator,
        _,
    ) = build_system()

    task = Task(
        task_id="task-2",
        description="Execute test task",
    )

    result = orchestrator.execute(task)

    assert result.status == "completed"
    assert result.task_id == "task-2"
    assert result.worker_id == "worker_1"
    assert result.error is None
    assert "task-2" in worker.tasks


def test_execution_result_is_recorded():
    (
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        orchestrator,
        _,
    ) = build_system()

    task = Task(
        task_id="task-3",
        description="Result test",
    )

    result = orchestrator.execute(task)
    stored = orchestrator.get_result("task-3")

    assert stored is result
    assert stored.status == "completed"
    assert orchestrator.is_successful("task-3")
    assert not orchestrator.is_failed("task-3")


def test_execution_summary_counts_successful_tasks():
    (
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        orchestrator,
        _,
    ) = build_system()

    orchestrator.execute(
        Task(
            task_id="task-4",
            description="First task",
        )
    )

    orchestrator.execute(
        Task(
            task_id="task-5",
            description="Second task",
        )
    )

    summary = orchestrator.summary()

    assert summary["total"] == 2
    assert summary["successful"] == 2
    assert summary["failed"] == 0


def test_invalid_task_is_rejected():
    (
        _,
        _,
        _,
        _,
        _,
        controller,
        _,
        _,
        _,
    ) = build_system()

    with pytest.raises(ValueError):
        controller.execute_task(None)


def test_empty_task_description_is_rejected():
    (
        _,
        _,
        _,
        _,
        _,
        controller,
        _,
        _,
        _,
    ) = build_system()

    task = Task(
        task_id="task-6",
        description="",
    )

    with pytest.raises(ValueError):
        controller.execute_task(task)


def test_system_status_is_available():
    (
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        orchestrator,
        status,
    ) = build_system()

    task = Task(
        task_id="task-7",
        description="Status test",
    )

    orchestrator.execute(task)

    current_status = status.get_status()

    assert "execution" in current_status
    assert "results" in current_status
    assert "ready" in current_status
    assert current_status["results"]["total"] == 1


def test_failures_are_detected():
    registry = WorkerExecutionRegistry()

    worker = FailingWorker()

    registry.register(
        WorkerExecutionAdapter(
            worker_id="worker_fail",
            worker=worker,
        )
    )

    coordinator = WorkerExecutionCoordinator(
        registry=registry,
    )

    engine = OdinExecutionEngine(
        worker_pool=None,
    )

    engine.register_handler(
        worker_id="worker_fail",
        handler=worker,
    )

    service = SupervisorExecutionService(
        execution_engine=engine,
        coordinator=coordinator,
    )

    controller = SupervisorExecutionController(
        execution_service=service,
    )

    result_service = SupervisorExecutionResultService()

    orchestrator = SupervisorExecutionOrchestrator(
        controller=controller,
        result_service=result_service,
    )

    task = Task(
        task_id="task-fail",
        description="Failure test",
    )

    result = orchestrator.execute(
        task,
        worker_id="worker_fail",
    )

    assert result.status == "error"
    assert result.error is not None
    assert orchestrator.is_failed("task-fail")
    assert result_service.count_failed() == 1


def test_multiple_tasks_are_tracked():
    (
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        orchestrator,
        status,
    ) = build_system()

    for index in range(5):
        orchestrator.execute(
            Task(
                task_id=f"task-{index}",
                description=f"Task {index}",
            )
        )

    summary = status.summary()

    assert summary["ready"] is True
    assert summary["total_executions"] == 5
    assert summary["successful"] == 5
    assert summary["failed"] == 0
    assert summary["has_failures"] is False
