import pytest

from src.supervisor.task import Task
from src.worker_4.task_executor import Worker4TaskExecutor


class MockHandler:
    def __init__(self, result="completed"):
        self.result = result

    def execute(self, task):
        return self.result


class FailingHandler:
    def execute(self, task):
        raise RuntimeError("Execution failed")


def create_assigned_task() -> Task:
    task = Task(
        task_id="task-001",
        description="Execute Worker 4 task",
    )
    task.assign("worker_4")
    return task


def test_executor_completes_task_successfully():
    executor = Worker4TaskExecutor()
    task = create_assigned_task()
    handler = MockHandler(result="success")

    result = executor.execute(task, handler)

    assert result == "success"
    assert task.status == "completed"
    assert task.metadata["result"] == "success"


def test_executor_starts_task_before_execution():
    executor = Worker4TaskExecutor()
    task = create_assigned_task()

    class StatusHandler:
        def execute(self, received_task):
            assert received_task.status == "running"
            return "ok"

    result = executor.execute(task, StatusHandler())

    assert result == "ok"
    assert task.status == "completed"


def test_executor_rejects_invalid_task():
    executor = Worker4TaskExecutor()

    with pytest.raises(TypeError):
        executor.execute("invalid_task", MockHandler())


def test_executor_rejects_task_for_another_worker():
    executor = Worker4TaskExecutor()

    task = Task(
        task_id="task-001",
        description="Wrong worker task",
    )
    task.assign("worker_1")

    with pytest.raises(ValueError):
        executor.execute(task, MockHandler())


def test_executor_rejects_unassigned_task():
    executor = Worker4TaskExecutor()
    task = Task(
        task_id="task-001",
        description="Unassigned task",
    )

    with pytest.raises(ValueError):
        executor.execute(task, MockHandler())


def test_executor_requires_valid_handler():
    executor = Worker4TaskExecutor()
    task = create_assigned_task()

    with pytest.raises(ValueError):
        executor.execute(task, None)


def test_executor_requires_execute_method():
    executor = Worker4TaskExecutor()
    task = create_assigned_task()

    class InvalidHandler:
        pass

    with pytest.raises(ValueError):
        executor.execute(task, InvalidHandler())


def test_executor_marks_task_as_failed_on_error():
    executor = Worker4TaskExecutor()
    task = create_assigned_task()

    with pytest.raises(RuntimeError, match="Execution failed"):
        executor.execute(task, FailingHandler())

    assert task.status == "failed"
    assert task.metadata["error"] == "Execution failed"


def test_executor_returns_handler_result():
    executor = Worker4TaskExecutor()
    task = create_assigned_task()
    handler = MockHandler(result={"status": "ok"})

    result = executor.execute(task, handler)

    assert result == {"status": "ok"}
