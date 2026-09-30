import pytest

from src.supervisor.task import Task
from src.worker_2.task_executor import Worker2TaskExecutor


class MockHandler:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error

    def execute(self, task):
        if self.error is not None:
            raise self.error

        return self.result


def create_assigned_task():
    task = Task(
        task_id="task-001",
        description="Execute test task",
    )
    task.assign("worker_2")
    return task


def test_executor_returns_handler_result():
    executor = Worker2TaskExecutor()
    task = create_assigned_task()
    handler = MockHandler(result="completed")

    result = executor.execute(task, handler)

    assert result == "completed"


def test_executor_completes_task():
    executor = Worker2TaskExecutor()
    task = create_assigned_task()
    handler = MockHandler(result="success")

    executor.execute(task, handler)

    assert task.status == "completed"
    assert task.metadata["result"] == "success"


def test_executor_rejects_invalid_task():
    executor = Worker2TaskExecutor()
    handler = MockHandler(result="success")

    with pytest.raises(TypeError):
        executor.execute("invalid_task", handler)


def test_executor_rejects_task_for_other_worker():
    executor = Worker2TaskExecutor()

    task = Task(
        task_id="task-001",
        description="Wrong worker task",
    )
    task.assign("worker_1")

    handler = MockHandler(result="success")

    with pytest.raises(ValueError):
        executor.execute(task, handler)


def test_executor_rejects_unassigned_task():
    executor = Worker2TaskExecutor()

    task = Task(
        task_id="task-001",
        description="Unassigned task",
    )

    handler = MockHandler(result="success")

    with pytest.raises(ValueError):
        executor.execute(task, handler)


def test_executor_rejects_missing_handler():
    executor = Worker2TaskExecutor()
    task = create_assigned_task()

    with pytest.raises(ValueError):
        executor.execute(task, None)


def test_executor_records_task_error():
    executor = Worker2TaskExecutor()
    task = create_assigned_task()
    error = RuntimeError("Execution failed")
    handler = MockHandler(error=error)

    with pytest.raises(RuntimeError):
        executor.execute(task, handler)

    assert task.status == "failed"
    assert task.metadata["error"] == "Execution failed"


def test_executor_starts_task_before_execution():
    executor = Worker2TaskExecutor()
    task = create_assigned_task()

    class StatusHandler:
        def execute(self, received_task):
            assert received_task.status == "running"
            return "done"

    result = executor.execute(task, StatusHandler())

    assert result == "done"
    assert task.status == "completed"
