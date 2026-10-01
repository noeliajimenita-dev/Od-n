from src.supervisor.task_execution_result import TaskExecutionResult


def test_result_stores_task_information():
    result = TaskExecutionResult(
        task_id="task-001",
        status="completed",
        output="success",
    )

    assert result.task_id == "task-001"
    assert result.status == "completed"
    assert result.output == "success"
    assert result.error is None


def test_completed_result_is_success():
    result = TaskExecutionResult(
        task_id="task-001",
        status="completed",
    )

    assert result.is_success is True
    assert result.is_failure is False


def test_failed_result_is_failure():
    result = TaskExecutionResult(
        task_id="task-002",
        status="failed",
        error="Execution failed",
    )

    assert result.is_success is False
    assert result.is_failure is True
    assert result.error == "Execution failed"


def test_result_accepts_metadata():
    result = TaskExecutionResult(
        task_id="task-003",
        status="completed",
        metadata={"worker": "worker_1"},
    )

    assert result.metadata["worker"] == "worker_1"


def test_result_adds_metadata():
    result = TaskExecutionResult(
        task_id="task-004",
        status="completed",
    )

    result.add_metadata("worker", "worker_2")
    result.add_metadata("duration", 15)

    assert result.metadata == {
        "worker": "worker_2",
        "duration": 15,
    }


def test_result_rejects_empty_metadata_key():
    result = TaskExecutionResult(
        task_id="task-005",
        status="completed",
    )

    try:
        result.add_metadata("", "value")
        assert False
    except ValueError as exc:
        assert str(exc) == "Metadata key cannot be empty"


def test_result_serializes_to_dict():
    result = TaskExecutionResult(
        task_id="task-006",
        status="completed",
        output={"message": "done"},
        metadata={"worker": "worker_1"},
    )

    data = result.to_dict()

    assert data == {
        "task_id": "task-006",
        "status": "completed",
        "output": {"message": "done"},
        "error": None,
        "metadata": {
            "worker": "worker_1",
        },
    }


def test_result_to_dict_copies_metadata():
    result = TaskExecutionResult(
        task_id="task-007",
        status="completed",
        metadata={"worker": "worker_1"},
    )

    data = result.to_dict()
    data["metadata"]["worker"] = "changed"

    assert result.metadata["worker"] == "worker_1"


def test_failed_result_serializes_error():
    result = TaskExecutionResult(
        task_id="task-008",
        status="failed",
        error="Worker unavailable",
    )

    data = result.to_dict()

    assert data["status"] == "failed"
    assert data["error"] == "Worker unavailable"
