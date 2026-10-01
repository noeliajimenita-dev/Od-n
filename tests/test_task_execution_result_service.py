import pytest

from src.supervisor.task import Task
from src.supervisor.task_execution_result_service import (
    TaskExecutionResultService,
)


def create_task(task_id: str = "task-001") -> Task:
    return Task(
        task_id=task_id,
        description=f"Task {task_id}",
    )


def test_service_starts_empty():
    service = TaskExecutionResultService()

    assert service.count() == 0
    assert service.list_results() == []
    assert service.summary() == {
        "total": 0,
        "completed": 0,
        "failed": 0,
    }


def test_service_records_success():
    service = TaskExecutionResultService()
    task = create_task()

    result = service.record_success(
        task,
        output="completed successfully",
    )

    assert result.task_id == "task-001"
    assert result.status == "completed"
    assert result.output == "completed successfully"
    assert result.is_success is True


def test_service_records_success_metadata():
    service = TaskExecutionResultService()
    task = create_task()

    result = service.record_success(
        task,
        output="done",
        metadata={"worker": "worker_1"},
    )

    assert result.metadata == {
        "worker": "worker_1",
    }


def test_service_records_failure():
    service = TaskExecutionResultService()
    task = create_task()

    result = service.record_failure(
        task,
        "Worker execution failed",
    )

    assert result.task_id == "task-001"
    assert result.status == "failed"
    assert result.error == "Worker execution failed"
    assert result.is_failure is True


def test_service_records_failure_metadata():
    service = TaskExecutionResultService()
    task = create_task()

    result = service.record_failure(
        task,
        "Execution error",
        metadata={"worker": "worker_2"},
    )

    assert result.metadata == {
        "worker": "worker_2",
    }


def test_service_retrieves_result():
    service = TaskExecutionResultService()
    task = create_task()

    service.record_success(
        task,
        output="success",
    )

    result = service.get("task-001")

    assert result is not None
    assert result.output == "success"


def test_service_returns_none_for_unknown_task():
    service = TaskExecutionResultService()

    assert service.get("unknown-task") is None
    assert service.has_result("unknown-task") is False


def test_service_detects_existing_result():
    service = TaskExecutionResultService()
    task = create_task()

    service.record_success(task)

    assert service.has_result("task-001") is True


def test_service_lists_results():
    service = TaskExecutionResultService()

    service.record_success(
        create_task("task-001"),
        output="first",
    )
    service.record_failure(
        create_task("task-002"),
        error="second failed",
    )

    results = service.list_results()

    assert len(results) == 2
    assert results[0].task_id == "task-001"
    assert results[1].task_id == "task-002"


def test_service_counts_results():
    service = TaskExecutionResultService()

    service.record_success(create_task("task-001"))
    service.record_failure(
        create_task("task-002"),
        "failed",
    )

    assert service.count() == 2


def test_service_returns_summary():
    service = TaskExecutionResultService()

    service.record_success(create_task("task-001"))
    service.record_success(create_task("task-002"))
    service.record_failure(
        create_task("task-003"),
        "failed",
    )

    assert service.summary() == {
        "total": 3,
        "completed": 2,
        "failed": 1,
    }


def test_service_rejects_invalid_task_on_success():
    service = TaskExecutionResultService()

    with pytest.raises(
        TypeError,
        match="Expected a Task instance",
    ):
        service.record_success("invalid_task")


def test_service_rejects_invalid_task_on_failure():
    service = TaskExecutionResultService()

    with pytest.raises(
        TypeError,
        match="Expected a Task instance",
    ):
        service.record_failure(
            "invalid_task",
            "error",
        )


def test_service_rejects_empty_failure_message():
    service = TaskExecutionResultService()
    task = create_task()

    with pytest.raises(
        ValueError,
        match="Error message cannot be empty",
    ):
        service.record_failure(task, "   ")


def test_service_normalizes_failure_message():
    service = TaskExecutionResultService()
    task = create_task()

    result = service.record_failure(
        task,
        "  Worker failed  ",
    )

    assert result.error == "Worker failed"


def test_service_replaces_previous_result_for_same_task():
    service = TaskExecutionResultService()
    task = create_task()

    service.record_failure(
        task,
        "first failure",
    )

    service.record_success(
        task,
        output="recovered",
    )

    result = service.get("task-001")

    assert result is not None
    assert result.status == "completed"
    assert result.output == "recovered"
    assert service.count() == 1
